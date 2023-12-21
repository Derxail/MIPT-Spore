import pygame
import numpy as np
import math

COLORS = {0: (218, 189, 171), 1: (244, 164, 96), 2: (11, 91, 159), 3: (50, 50, 0)}
TILE_TYPES = {"air": 0, "wall": 1, "water": 2, "bedrock": 3}

class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask):
        self.position = coords
        self.vx = 0
        self.vy = 0
        self.image = image.copy()
        self.collider = collider
        self.angle = 0

    def get_image(self):
        return self.image

    def collision(self, collider, offset):
        if self.collider.overlap(collider, offset) is not None:
            return True
        return False

    def move(self, map, vx, vy):
        pass

    def receive_hit(self, power):
        pass

    def set_speed(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def update(self, map, dt):
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
                if (tile.types[ind] == TILE_TYPES["wall"] or
                        tile.types[ind] == TILE_TYPES["bedrock"]):
                    if self.collision(tile.colliders[ind], offset):
                        overlap = self.collider.overlap_mask(tile.colliders[ind], offset)
                        collision_point = overlap.centroid()
                        center_to_collision_vector = np.array([size / 2, size / 2]) - np.array(collision_point)
                        normal_vect = center_to_collision_vector / np.linalg.norm(center_to_collision_vector)
                        radius_vector = (size / 2) * normal_vect
                        delta = radius_vector - center_to_collision_vector
                        self.position[0] += int(delta[1] * 2)
                        self.position[1] += int(delta[0] * 2)
                elif tile.types[ind] == TILE_TYPES["water"]:
                    area = self.collider.overlap_area(tile.colliders[ind], offset)
                    if area > 10:
                        dx = self.vx * dt / 3
                        dy = self.vy * dt / 3
        #как это работает я не знаю, но лучше не трогать
        self.position[0] += dy
        self.position[1] += dx
        map.write_object(self)

    def receive_hit(self, power):
        self.hp -= power
        print("hit recieved", self.hp)
        if self.hp <= 0:
            self.alive = False

class Projectile(Entity):
    def __init__(self, coords, image, collider_resolution, vx, vy, owner_id, ang_speed=0, power=1):
        surface = pygame.Surface([collider_resolution, collider_resolution], pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255),
                           (collider_resolution / 2, collider_resolution / 2), collider_resolution / 2)
        collider = pygame.mask.from_surface(surface)
        super().__init__(coords, image, collider)
        self.flies = True
        self.vx = vx
        self.vy = vy
        self.owner_id = owner_id
        self.ang_speed = ang_speed
        self.power = power

    def update(self, map, dt):
        self.angle += dt * self.ang_speed

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
                if (tile.types[ind] == TILE_TYPES["wall"]
                        or tile.types[ind] == TILE_TYPES["bedrock"]):

                    if self.collision(tile.colliders[ind], offset):
                        self.flies = False
                        if tile.types[ind] == TILE_TYPES["wall"]:
                            tile.recieve_hit(self.power)
                            if tile.hp <= 0:
                                for ind1 in range(len(tile.types)):
                                    tile.types[ind1] = 0
                                    tile.codes[ind1] = "1111"
                                    tile.set_color(COLORS[TILE_TYPES["air"]], COLORS[TILE_TYPES["air"]], ind1)

            for object in tile.objects:
                offset = (object.position[1] - (self.position[1] + dy),
                          object.position[0] - (self.position[0] + dx))
                if id(object) != self.owner_id:
                    if self.collision(object.collider, offset):  # FIX!!!
                        self.flies = False
                        object.receive_hit(self.power)

        # как это работает я не знаю, но лучше не трогать
        self.position[0] += dy
        self.position[1] += dx
        map.write_object(self)

    def receive_hit(self, power):
        self.flies = False
