import random
import pygame
import numpy as np
import UI
import math

COLORS = {0: (218, 189, 171), 1: (244, 164, 96), 2: (11, 91, 159), 3: (50, 50, 0)}
PARTICLES_COLORS = {"blood": (230, 0, 20), "wall": (250, 165, 109), "bedrock": (60, 60, 0)}
TILE_TYPES = {"air": 0, "wall": 1, "water": 2, "bedrock": 3}
PARTICLES_COUNT = 30

class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask, vx = 0, vy = 0):
        self.position = coords
        if image is not None:
            self.image = image.copy()
        self.collider = collider
        self.vx = vx
        self.vy = vy
        self.angle = 0

    def get_image(self):
        return self.image

    def collision(self, collider, offset):
        if self.collider.overlap(collider, offset) is not None:
            return True
        return False

    def move(self, map, dt):
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
        self.health_bar = UI.HealthBar(
            hp,
            hp,
            100,
            20,
            (255,0,0),
            (0,0,0)
        )

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

    def receive_hit(self, power, by_player: bool, killer_callback):
        self.hp -= power
        self.health_bar.set_value(self.hp)
        print("hit recieved", self.hp)
        if self.hp <= 0:
            self.alive = False
            if by_player is True:
                killer_callback()

    def update(self, map, dt):
        pass

class Projectile(Entity):
    def __init__(self, coords, image, collider_resolution, vx, vy,
                 owner_id, player_id, kill_callback, ang_speed=0, power=1):
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
        self.player_id = player_id
        self.kill_callback = kill_callback

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
                            map.spawn_particles_bundle(
                                PARTICLES_COUNT,
                                PARTICLES_COLORS["wall"],
                                [float(self.position[0]), float(self.position[1])]
                            )
                            tile.recieve_hit(self.power)
                            if tile.hp <= 0:
                                for ind1 in range(len(tile.types)):
                                    tile.types[ind1] = 0
                                    tile.codes[ind1] = "1111"
                                    tile.set_color(COLORS[TILE_TYPES["air"]], COLORS[TILE_TYPES["air"]], ind1)
                        if tile.types[ind] == TILE_TYPES["bedrock"]:
                            map.spawn_particles_bundle(
                                PARTICLES_COUNT,
                                PARTICLES_COLORS["bedrock"],
                                [float(self.position[0]), float(self.position[1])]
                            )

            for object in tile.objects:
                offset = (object.position[1] - (self.position[1] + dy),
                          object.position[0] - (self.position[0] + dx))
                if id(object) != self.owner_id and isinstance(object, Creature):
                    if self.collision(object.collider, offset):  # FIX!!!
                        self.flies = False
                        map.spawn_particles_bundle(
                            PARTICLES_COUNT,
                            PARTICLES_COLORS["blood"],
                            [float(self.position[0]), float(self.position[1])]
                        )
                        if id(object != self.player_id and self.owner_id == self.player_id):
                            object.receive_hit(self.power, True, self.kill_callback)
                        else:
                            object.receive_hit(self.power, False, self.kill_callback)




        # как это работает я не знаю, но лучше не трогать
        self.position[0] += dy
        self.position[1] += dx
        map.write_object(self)

    def receive_hit(self, power):
        self.flies = False

class Particle:
    def __init__(self, coords: list, color, lifetime, speed):
        radius = random.randint(2, 5)
        v = (speed / radius)*(random.random()+0.2)
        angle = random.random() * 2 * math.pi
        self.position = coords
        self.vx = v * math.cos(angle)
        self.vy = v * math.sin(angle)
        self.radius = radius
        self.variated_color = (
            min(255, color[0] + random.randint(0, 20)),
            min(255, color[1] + random.randint(0, 20)),
            min(255, color[2] + random.randint(0, 20))
        )
        self.lifetime = lifetime
        self.alive = True

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
        self.position[0] += self.vx * dt
        self.position[1] += self.vy * dt
