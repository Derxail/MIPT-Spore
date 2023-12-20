import pygame
import numpy as np
import math


class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask):
        self.position = coords
        self.image = image.copy()
        self.collider = collider

    def get_image(self):
        return self.image

    def collision(self, collider, offset):
        if self.collider.overlap(collider, offset) is not None:
            return True
        return False

    def move(self, map, vx, vy):
        pass

    def receive_hit(self):
        pass


class Creature(Entity):
    def __init__(self, coords: list, image: pygame.Surface, collider_resolution, hp=3):
        surface = pygame.Surface([collider_resolution, collider_resolution], pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255),
                           (collider_resolution / 2, collider_resolution / 2), collider_resolution / 2)
        collider = pygame.mask.from_surface(surface)
        super().__init__(coords, image, collider)
        self.hp = hp
        self.alive = True
        self.angle = 0

    def move(self, map, vx, vy):
        size = self.collider.get_size()[0]
        occupied_tiles = map.get_occupied_tiles(self)
        map.remove_object(self)
        dx = vx
        dy = vy
        for position in occupied_tiles:
            tile = map.get(position[0], position[1])
            offset = (position[1] * map.resolution - (self.position[1] + vy),
                      position[0] * map.resolution - (self.position[0] + vx))
            for ind in range(len(tile.colliders)):
                if tile.types[ind] == 1:
                    if self.collision(tile.colliders[ind], offset):
                        overlap = self.collider.overlap_mask(tile.colliders[ind],
                                                             (position[1] * map.resolution - (self.position[1] + vy),
                                                              position[0] * map.resolution - (self.position[0] + vx)))
                        collision_point = overlap.centroid()
                        center_to_collision_vector = np.array([size / 2, size / 2]) - np.array(collision_point)
                        normal_vect = center_to_collision_vector / np.linalg.norm(center_to_collision_vector)
                        radius_vector = (size / 2) * normal_vect
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

    def receive_hit(self):
        self.hp -= 1

    def targetting(self, event):
        if event:
            self.angle = math.atan2((event.pos[1]-self.position[1]), (event.pos[0]-self.position[0]))



class Projectile(Entity):
    def __init__(self, coords, image, collider_resolution, vx, vy):
        surface = pygame.Surface([collider_resolution, collider_resolution], pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255),
                           (collider_resolution / 2, collider_resolution / 2), collider_resolution / 2)
        collider = pygame.mask.from_surface(surface)
        super().__init__(coords, image, collider)
        self.flies = True
        self.vx = vx
        self.vy = vy

    def move(self, map):
        occupied_tiles = map.get_occupied_tiles(self)
        map.remove_object(self)
        for position in occupied_tiles:
            tile = map.get(position[0], position[1])
            for ind in range(len(tile.colliders)):
                if tile.types[ind] == 1:
                    if self.collision(tile.colliders[ind]):
                        self.flies = False
            for object in tile.objects:
                if self.collision(object.collider):
                    self.flies = False
                    object.receive_hit()
        self.position[0] += self.vx
        self.position[1] += self.vy
        map.write_object(self)

    def receive_hit(self):
        self.flies = False
