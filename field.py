import random
import copy
import entities
import utils
import math
import pygame
from random import randint as rd
from noise import generate_noise

TILE_TYPES = {"air": 0, "wall": 1, "water": 2, "bedrock": 3}

def nearby_any(x, y, grid, element):
    return (grid[x+1][y] == element or grid[x][y+1] or
            grid[x-1][y] == element or grid[x][y-1])

def nearby_all(x, y, grid, element):
    return (grid[x+1][y] == element and grid[x][y+1] and
            grid[x-1][y] == element and grid[x][y-1])

def generate_masks(size: int, masks: dict):
    """
    Поле представлено квадратной сеткой. Каждой вершине сопоставляется число. Если число отлично от нуля, то
    данная вершина считается находящейся внутри некоторой поверхности и отделяется от нулевых вершин.
    Данная функция создаёт данные паттерны - 16 вариантов.
    """

    # size - размер маски, т. е. тайла поля
    # masks - словарь, хранящий маски по коду
    half = size / 2  # середина стороны квадрата маски
    for p1 in 0, 1:
        for p2 in 0, 1:
            for p3 in 0, 1:
                for p4 in 0, 1:
                    code = str(p1) + str(p2) + str(p3) + str(p4)
                    surface = pygame.Surface([size, size], pygame.SRCALPHA)
                    # Числа кода соответствуют вершинам квадратов сетки: первое - левый верхний,
                    # второе - правый верхний, третье - левый нижний, четвёртое - правый нижний
                    if code == '1000':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [half, 0], [0, half]])
                    elif code == '0100':
                        pygame.draw.polygon(surface, (255, 255, 255), [[half, 0], [size, 0], [size, half]])
                    elif code == '0010':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, size], [0, half], [half, size]])
                    elif code == '0001':
                        pygame.draw.polygon(surface, (255, 255, 255), [[size, size], [half, size], [size, half]])

                    elif code == '0111':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, half], [0, size],
                                                                       [size, size], [size, 0], [half, 0]])
                    elif code == '1011':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [0, size],
                                                                       [size, size], [size, half], [half, 0]])
                    elif code == '1101':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [0, half],
                                                                       [half, size], [size, size], [size, 0]])
                    elif code == '1110':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [0, size],
                                                                       [half, size], [size, half], [size, 0]])
                    elif code == '1100':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [size, 0], [size, half], [0, half]])
                    elif code == '0011':
                        pygame.draw.polygon(surface, (255, 255, 255), [[size, size], [size, half],
                                                                       [0, half], [0, size]])
                    elif code == '1010':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [half, 0], [half, size], [0, size]])
                    elif code == '0101':
                        pygame.draw.polygon(surface, (255, 255, 255), [[size, 0], [half, 0], [half, size], [size, size]])
                    elif code == '1001':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [half, 0], [0, half]])
                        pygame.draw.polygon(surface, (255, 255, 255), [[size, size], [half, size], [size, half]])
                    elif code == '0110':
                        pygame.draw.polygon(surface, (255, 255, 255), [[half, 0], [size, 0], [size, half]])
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, size], [0, half], [half, size]])
                    elif code == '1111':
                        pygame.draw.polygon(surface, (255, 255, 255), [[0, 0], [0, size], [size, size], [size, 0]])
                    masks[code] = pygame.mask.from_surface(surface)


class Tile:
    """
    Клетка поля. Здесь хранится информация об объектах, расположенных в данной ячейке поля.
    polygons - полигоны, отделяющие вершины с отличными от нуля значениями
    types - типы вершин тайла: 0 - пустая вершина, 1 - препятствие, 2 - вода.
    """

    def __init__(self, size, masks: dict, codes: list, types: list, hp=10):
        self.colliders = []
        for i in range(len(codes)):
            self.colliders.append(masks[codes[i]])
        self.codes = codes
        self.types = types
        self._image = pygame.Surface([size, size])
        self.size = size
        self.hp = hp
        self._image.fill((218, 189, 171))
        self.objects = []

    def recieve_hit(self, power):
        self.hp -= power

    def set_color(self, color, back_color, layer_index):
        self._image.fill(back_color)
        print(color)
        utils.gen_polygon(
                self._image,
                self.codes[layer_index],
                color,
                self.size
            )

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image.copy()

    def add(self, object):
        self.objects.append(object)

    def remove(self, object):
        try:
            self.objects.remove(object)
        except ValueError:
            print("Out!", object.position)


class Map:
    def __init__(self, size_x: int, size_y: int, tile_resolution: int, scale_factor, spawn_points_cnt=10):
        # size_x - горизонтальный размер карты в клетках
        # size_y - вертикальный размер карты в клетках
        # tile_resolution - ширина клетки поля в пикселях системы координат карты
        self.vertex_grid = [[-1] * size_x for _ in range(size_y)]
        self.size = (size_y, size_x)
        self.spawn_points_cnt = spawn_points_cnt
        self.resolution = tile_resolution
        self._masks = dict()
        generate_masks(self.resolution, self._masks)
        self.spawn_points = list()
        self._fill_grid()
        self.scale_factor = scale_factor
        self.particles = []


    def _fill_grid(self):
        perlin_noise = generate_noise(self.size[0], self.size[1], period = 15)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if i == 0 or j == 0 or i == self.size[0] - 1 or j == self.size[1] - 1:
                    self.vertex_grid[i][j] = TILE_TYPES["bedrock"]
                else:
                    if perlin_noise[i][j] >= 0.06:
                        self.vertex_grid[i][j] = TILE_TYPES["wall"]
                    elif perlin_noise[i][j] >= -0.2:
                        self.vertex_grid[i][j] = TILE_TYPES["air"]
                    else:
                        self.vertex_grid[i][j] = TILE_TYPES["water"]

        for i in range(2, self.size[0] - 2):
            for j in range(2, self.size[1] - 2):
                if nearby_all(i, j, self.vertex_grid, 0):
                    self.vertex_grid[i][j] = TILE_TYPES["air"]
        spawn_points_s = set()
        while len(spawn_points_s) < self.spawn_points_cnt:
            i = random.randint(2, self.size[0] - 2)
            j = random.randint(2, self.size[1] - 2)
            if nearby_all(i, j, self.vertex_grid, 0):
                spawn_points_s.add(
                    (
                        (i + 0.5)*self.resolution,
                        (j + 0.5)*self.resolution
                    )
                )
        self.spawn_points.clear()
        for el in spawn_points_s:
            self.spawn_points.append([el[0], el[1]])

        self.face_grid = [[-1] * (self.size[1] - 1) for _ in range(self.size[0] - 1)]
        for i in range(self.size[0] - 1):
            for j in range(self.size[1] - 1):
                verts = [self.vertex_grid[i][j], self.vertex_grid[i][j + 1],
                         self.vertex_grid[i + 1][j], self.vertex_grid[i + 1][j + 1]]
                types = set(verts)
                if TILE_TYPES["bedrock"] in types:
                    types = [TILE_TYPES["bedrock"]]
                else:
                    types = list(types)

                codes = [''] * len(types)
                for vertex in verts:
                    for ind in range(len(types)):
                        if vertex == types[ind]:
                            codes[ind] += '1'
                        else:
                            codes[ind] += '0'
                self.face_grid[i][j] = Tile(self.resolution, self._masks, codes, types)

    def get(self, i, j, exception_size=60):
        if i < 0 or i >= self.size[0] - 1 or j < 0 or j >= self.size[1] - 1:
            return Tile(exception_size, self._masks, [], [])
        return self.face_grid[i][j]

    def get_spawn_points(self):
        return self.spawn_points

    def get_occupied_tiles(self, object):
        if object.collider is not None:
            size = object.collider.get_size()
        else:
            size = [0, 0]
        innate_pos = (round(object.position[0]) // self.resolution, round(object.position[1]) // self.resolution)
        res = [innate_pos]
        for direction in (0, size[1]), (size[0], 0), (size[0], size[1]):
            corner_pos = ((round(object.position[0]) + direction[0]) // self.resolution,
                          (round(object.position[1]) + direction[1]) // self.resolution)
            if corner_pos != innate_pos:
                res.append(corner_pos)
        return res

    def write_object(self, object):
        occupied_tiles = self.get_occupied_tiles(object)
        for position in occupied_tiles:
            self.get(position[0], position[1]).add(object)

    def remove_object(self, object):
        occupied_tiles = self.get_occupied_tiles(object)
        for position in occupied_tiles:
            self.get(position[0], position[1]).remove(object)

    def spawn_particles_bundle(self, count, color, position, lifetime = 1, speed = 500):
        for i in range(count):
            self.particles.append(
                entities.Particle(copy.deepcopy(position), copy.deepcopy(color), float(lifetime), float(speed))
            )

    def update(self, dt):
        ind = 0
        while ind < len(self.particles):
            particle = self.particles[ind]
            if not particle.alive:
                self.particles.remove(particle)
            else:
                particle.update(dt)
                ind += 1
