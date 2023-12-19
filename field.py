import pygame
from random import randint as rd
from noise import generate_noise

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

    def __init__(self, size, masks: dict, codes: list, types: list):
        self.colliders = []
        for i in range(len(codes)):
            self.colliders.append(masks[codes[i]])
        self.codes = codes
        self.types = types
        self._image = pygame.Surface([size, size])
        self._image.fill((218, 189, 171))
        self.objects = []

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image.copy()



class Map:
    def __init__(self, size_x: int, size_y: int, grid_step: int):
        # size_x - горизонтальный размер карты в клетках
        # size_y - вертикальный размер карты в клетках
        # grid_step - ширина клетки поля в пикселях
        self.vertex_grid = [[-1] * size_x for _ in range(size_y)]
        self.size = (size_y, size_x)
        self.grid_step = grid_step
        self._masks = dict()
        generate_masks(self.grid_step, self._masks)
        self._fill_grid()

    def _fill_grid(self):
        perlin_noise = generate_noise(self.size[0], self.size[1], period = 15)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if i == 0 or j == 0 or i == self.size[0] - 1 or j == self.size[1] - 1:
                    self.vertex_grid[i][j] = 1
                else:
                    if perlin_noise[i][j] >= 0.06:
                        self.vertex_grid[i][j] = 1
                    elif perlin_noise[i][j] >= -0.2:
                        self.vertex_grid[i][j] = 0
                    else:
                        self.vertex_grid[i][j] = 2
        for i in range(1, self.size[0] - 1):
            for j in range(1, self.size[1] - 1):
                if nearby_all(i, j, self.vertex_grid, 0):
                    self.vertex_grid[i][j] = 0
        self.face_grid = [[-1] * (self.size[1] - 1) for _ in range(self.size[0] - 1)]
        for i in range(self.size[0] - 1):
            for j in range(self.size[1] - 1):
                verts = [self.vertex_grid[i][j], self.vertex_grid[i][j + 1],
                         self.vertex_grid[i + 1][j], self.vertex_grid[i + 1][j + 1]]
                types = list(set(verts))
                codes = [''] * len(types)
                for vertex in verts:
                    for ind in range(len(types)):
                        if vertex == types[ind]:
                            codes[ind] += '1'
                        else:
                            codes[ind] += '0'
                self.face_grid[i][j] = Tile(self.grid_step, self._masks, codes, types)

    def get(self, i, j, exception_size=60):
        if i < 0 or i >= self.size[0] - 1 or j < 0 or j >= self.size[1] - 1:
            return Tile(exception_size, self._masks, [], [])
        return self.face_grid[i][j]
