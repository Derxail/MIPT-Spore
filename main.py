import pygame
import field
import frontend
import entities
import main_menu


WIDTH = 800
HEIGHT = 600
FPS = 30
TOKEN_SIZE = 60
TILE_SIZE = TOKEN_SIZE / 1.5
PLAYER_IMAGE = pygame.Surface([30, 30])
pygame.draw.circle(PLAYER_IMAGE, (255, 255, 255), (0, 0), 15)


class Game:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
        self.player = entities.Player((0, 0), PLAYER_IMAGE)
        self.camera = frontend.Camera(self.player.position, (WIDTH, HEIGHT))

'''def start(WIDTH, HEIGHT):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("FOPF survival")
    clock = pygame.time.Clock()

    map = field.Map(50, 20, 30)

    x = 0
    y = 0
    vx = 0
    vy = 0

    camera = frontend.Camera((x, y), (WIDTH, HEIGHT), 20)
    camera.render_tiles(map)

    running = True
    while running:
        vx = 0
        vy = 0
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH = event.w
                HEIGHT = event.h
                camera.update_view(WIDTH, HEIGHT)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            vx = -10
        if keys[pygame.K_d]:
            vx = 10
        if keys[pygame.K_w]:
            vy = -10
        if keys[pygame.K_s]:
            vy = 10
        x += vx
        y += vy
        camera.marching_squares(screen, map)
        camera.position = (x, y)

        pygame.display.flip()

    pygame.quit()

'''

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FOPF survival")
clock = pygame.time.Clock()



main_menu.Main_Menu()


map = field.Map(50, 20, 30)
x = 0
y = 0
vx = 0
vy = 0

camera = frontend.Camera((x, y), (WIDTH, HEIGHT), 20)
camera.render_tiles(map)
running = main_menu.is_True()

while running:
    vx = 0
    vy = 0
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH = event.w
            HEIGHT = event.h
            camera.update_view(WIDTH, HEIGHT)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        vx = -10
    if keys[pygame.K_d]:
        vx = 10
    if keys[pygame.K_w]:
        vy = -10
    if keys[pygame.K_s]:
        vy = 10
    if keys[pygame.K_z]:
        pygame.quit()
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("FOPF survival")
        clock = pygame.time.Clock()
        main_menu.Main_Menu()
    x += vx
    y += vy
    camera.marching_squares(screen, map)
    camera.position = (x, y)

    pygame.display.flip()

pygame.quit()
