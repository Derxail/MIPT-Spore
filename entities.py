import pygame


class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask):
        self.position = coords
        self.image = image
        self.collider = collider

    def get_image(self):
        return self.image


class Creature(Entity):
    def __init__(self, coords: list, image: pygame.Surface, size):
        surface = pygame.Surface([size, size], pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255), (size / 2, size / 2), size / 2)
        collider = pygame.mask.from_surface(surface)
        super().__init__(coords, image, collider)


class Enemy(Creature):
    pass


class Player(Creature):
    def __init__(self, coords: list, image: pygame.Surface, size):
        super().__init__(coords, image, size)
