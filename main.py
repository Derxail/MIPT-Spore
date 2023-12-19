import pygame
import field
import frontend
import entities


WIDTH = 800
HEIGHT = 600
FPS = 30
TOKEN_SIZE = 20
TILE_SIZE = int(TOKEN_SIZE * 1.5)
COLLIDER_RESOLUTION = 10
PLAYER_IMAGE = pygame.Surface([30, 30])
pygame.draw.circle(PLAYER_IMAGE, (255, 255, 255), (0, 0), 15)


class Game:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
        self.player = entities.Player([0, 0], PLAYER_IMAGE, COLLIDER_RESOLUTION)
        self.camera = frontend.Camera(self.player.position, (WIDTH, HEIGHT), TILE_SIZE)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FOPF survival")
clock = pygame.time.Clock()

map = field.Map(50, 20, COLLIDER_RESOLUTION)

x = 0
y = 0
vx = 0
vy = 0

game = Game()
camera = game.camera
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
