import pygame


class Entity:
    def __init__(self, collider_type):
        self.coords = (0, 0)
        self.rot = 0
        self.image = None

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.rot)
        rect = rotated_image.get_rect(center=self.coords)
        screen.blit(self.image, rect)

    def update(self, dt, objects):
        pass
