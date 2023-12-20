import pygame
import numpy as np


class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask):
        self.position = coords
        self.image = image.copy()
        self.collider = collider

    def get_image(self):
        return self.image

    def move(self, map, vx, vy):
        size = self.collider.get_size()
        occupied_tiles = map.get_occupied_tiles(self)
        map.remove_object(self)
        dx = vx
        dy = vy
        for position in occupied_tiles:
            tile = map.get(position[0], position[1])
            for ind in range(len(tile.colliders)):
                if tile.types[ind] == 1:
                    collision_point = self.collider.overlap(tile.colliders[ind],
                                                            (position[1] * map.resolution - (self.position[1] + vy),
                                                             position[0] * map.resolution - (self.position[0] + vx)))
                    if collision_point is not None:
                        overlap = self.collider.overlap_mask(tile.colliders[ind],
                                                             (position[1] * map.resolution - (self.position[1] + vy),
                                                              position[0] * map.resolution - (self.position[0] + vx)))
                        collision_point = overlap.centroid()
                        center_to_collision_vector = np.array([size[0] / 2, size[1] / 2]) - np.array(collision_point)
                        normal_vect = center_to_collision_vector / np.linalg.norm(center_to_collision_vector)
                        radius_vector = (size[0] / 2) * normal_vect
                        delta = radius_vector - center_to_collision_vector
                        self.position[0] += int(delta[1] * 2)
                        self.position[1] += int(delta[0] * 2)
                elif tile.types[ind] == 2:
                    area = self.collider.overlap_area(tile.colliders[ind],
                                                         (position[1] * map.resolution - (self.position[1]),
                                                          position[0] * map.resolution - (self.position[0])))
                    if area > 10:
                        dx = vx // 3
                        dy = vy // 3
        self.position[0] += dx
        self.position[1] += dy
        map.write_object(self)


class Creature(Entity):
    def __init__(self, coords: list, image: pygame.Surface, collider_resolution):
        surface = pygame.Surface([collider_resolution, collider_resolution], pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255),
                           (collider_resolution / 2, collider_resolution / 2), collider_resolution / 2)
        collider = pygame.mask.from_surface(surface)
        super().__init__(coords, image, collider)


class Enemy(Creature):
    pass


class Player(Creature):
    def __init__(self, coords: list, image: pygame.Surface, collider_resolution):
        super().__init__(coords, image, collider_resolution)
