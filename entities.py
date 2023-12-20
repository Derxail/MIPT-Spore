import pygame
import numpy as np
import math


class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask):
        self.position = coords
        self.vx = 0
        self.vy = 0
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

    def set_speed(self, vx, vy):
        self.vx = vx
        self.vy = vy


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

    def move(self, map, dt):
        size = self.collider.get_size()[0]
        occupied_tiles = map.get_occupied_tiles(self)
        map.remove_object(self)
        dx = self.vx * dt
        dy = self.vy * dt
        for position in occupied_tiles:
            tile = map.get(position[0], position[1])
            offset = (position[1] * map.resolution - (self.position[1] + dy),
                      position[0] * map.resolution - (self.position[0] + dx))
            for ind in range(len(tile.colliders)):
                if tile.types[ind] == 1:
                    if self.collision(tile.colliders[ind], offset):
                        overlap = self.collider.overlap_mask(tile.colliders[ind], offset)
                        collision_point = overlap.centroid()
                        center_to_collision_vector = np.array([size / 2, size / 2]) - np.array(collision_point)
                        normal_vect = center_to_collision_vector / np.linalg.norm(center_to_collision_vector)
                        radius_vector = (size / 2) * normal_vect
                        delta = radius_vector - center_to_collision_vector
                        self.position[0] += int(delta[1] * 2)
                        self.position[1] += int(delta[0] * 2)
                elif tile.types[ind] == 2:
                    area = self.collider.overlap_area(tile.colliders[ind], offset)
                    if area > 10:
                        dx = self.vx * dt / 3
                        dy = self.vy * dt / 3
        #как это работает я не знаю, но лучше не трогать
        self.position[0] += dy
        self.position[1] += dx
        map.write_object(self)

    def receive_hit(self):
        self.hp -= 1

    def targetting(self, event):
        if event:
            self.angle = math.atan2((event.pos[1]-self.position[1]), (event.pos[0]-self.position[0]))


class Enemy(Creature):
    def __init__(self,coords: list,
                 image: pygame.Surface,
                 collider_resolution,
                 hp=3
    ):
        super().__init__(coords, image, collider_resolution, hp)


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

    def move(self, map, dt):
        occupied_tiles = map.get_occupied_tiles(self)
        map.remove_object(self)
        for position in occupied_tiles:
            tile = map.get(position[0], position[1])
            for ind in range(len(tile.colliders)):
                if tile.types[ind] == 1:
                    if self.collision(tile.colliders[ind], (0, 0)): #FIX!!!
                        self.flies = False
            for object in tile.objects:
                if self.collision(object.collider, (0, 0)): #FIX!!!
                    self.flies = False
                    object.receive_hit()
        self.position[0] += self.vx * dt
        self.position[1] += self.vy * dt
        map.write_object(self)

    def receive_hit(self):
        self.flies = False
