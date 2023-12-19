import pygame


class Entity:
    def __init__(self, coords: list, image: pygame.Surface, collider: pygame.mask.Mask):
        self.position = coords
        self.image = image.copy()
        self.collider = collider

    def get_image(self):
        return self.image


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
