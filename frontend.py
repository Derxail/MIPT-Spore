import math
import entities
import pygame
import field
import utils
from math import ceil


class Camera:
    def __init__(self, position, view_size, scale):
        self.color = {0: (218, 189, 171), 1: (244, 164, 96), 2: (11, 91, 159), 3: (50, 50, 0)}
        self.position = position
        self.view_size = view_size
        self.tile_size = scale

    def render_tiles(self, map):
        for i in range(map.size[0] - 1):
            for j in range(map.size[1] - 1):
                tile = map.get(i, j)
                size = self.tile_size
                half = self.tile_size / 2
                surface = pygame.Surface([size, size])
                surface.fill(self.color[0])
                for ind in range(len(tile.types)):
                    code = tile.codes[ind]
                    if code == '1000':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [half, 0], [0, half]])
                    elif code == '0100':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[half, 0], [size, 0], [size, half]])
                    elif code == '0010':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, size], [0, half], [half, size]])
                    elif code == '0001':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[size, size], [half, size], [size, half]])

                    elif code == '0111':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, half], [0, size],
                                                                       [size, size], [size, 0], [half, 0]])
                    elif code == '1011':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [0, size],
                                                                       [size, size], [size, half], [half, 0]])
                    elif code == '1101':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [0, half],
                                                                       [half, size], [size, size], [size, 0]])
                    elif code == '1110':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [0, size],
                                                                       [half, size], [size, half], [size, 0]])
                    elif code == '1100':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [size, 0], [size, half], [0, half]])
                    elif code == '0011':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[size, size], [size, half],
                                                                       [0, half], [0, size]])
                    elif code == '1010':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [half, 0], [half, size], [0, size]])
                    elif code == '0101':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[size, 0], [half, 0], [half, size], [size, size]])
                    elif code == '1001':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [half, 0], [0, half]])
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[size, size], [half, size], [size, half]])
                    elif code == '0110':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[half, 0], [size, 0], [size, half]])
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, size], [0, half], [half, size]])
                    elif code == '1111':
                        pygame.draw.polygon(surface, self.color[tile.types[ind]], [[0, 0], [0, size], [size, size], [size, 0]])
                #pygame.draw.line(surface, (0, 0, 0), [0, 0], [0, size])
                #pygame.draw.line(surface, (0, 0, 0), [0, size], [size, size])
                #pygame.draw.line(surface, (0, 0, 0), [size, size], [size, 0])
                #pygame.draw.line(surface, (0, 0, 0), [size, 0], [0, 0])
                tile.set_image(surface)

    def marching_squares(self, screen: pygame.Surface, map: field.Map):
        repere = (self.position[0] - self.view_size[0] / 2, self.position[1] - self.view_size[1] // 2)
        start_square = (
            int((self.position[0] - self.view_size[0] / 2) / self.tile_size) - 1,
            int((self.position[1] - self.view_size[1] / 2) / self.tile_size) - 1)
        end_square = (
            ceil((self.position[0] + self.view_size[0] / 2) / self.tile_size),
            ceil((self.position[1] + self.view_size[1] / 2) / self.tile_size))
        objects_to_draw = set()
        for i in range(start_square[1], end_square[1] + 1):
            for j in range(start_square[0], end_square[0] + 1):
                tile = map.get(i, j, self.tile_size)
                background = tile.get_image()
                screen.blit(background, (j * self.tile_size - repere[0], i * self.tile_size - repere[1]))
                for object in tile.objects:
                    objects_to_draw.add(object)
        for object in objects_to_draw:
            if isinstance(object, entities.Creature):
                print(object.hp)

            i = object.position[0] * self.tile_size / map.resolution
            j = object.position[1] * self.tile_size / map.resolution
            screen.blit(
                utils.rotate_image(object.get_image(), -(object.angle/math.pi)*180),
                (j - repere[0], i - repere[1])
            )

    def draw(self, screen, map):
        self.marching_squares(screen, map)


    def update_view(self, width, height):
        self.view_size = (width, height)
