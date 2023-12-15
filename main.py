import pygame
import sys
import field

WIDTH = 600
HEIGHT = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spore")
clock = pygame.time.Clock()

running = True
i, j, k = 0, 0, 0
r = 0
x, y = 300, 300
image = pygame.image.load('bomb.png')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    pygame.display.flip()
