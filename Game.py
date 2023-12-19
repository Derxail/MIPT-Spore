import pygame
import field
import frontend
import entities


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 30
        self.TOKEN_SIZE = 20
        self.TILE_SIZE = int(self.TOKEN_SIZE * 1.5)
        self.COLLIDER_RESOLUTION = 10
        self.PLAYER_IMAGE = pygame.Surface([30, 30])
        pygame.draw.circle(
            self.PLAYER_IMAGE, (255, 255, 255),(0, 0), 15
        )
        self.enemies = []
        self.projectiles = []
        self.player = entities.Player(
            [0, 0], self.PLAYER_IMAGE, self.COLLIDER_RESOLUTION
        )
        self.camera = frontend.Camera(
            self.player.position,(self.WIDTH, self.HEIGHT), self.TILE_SIZE
        )
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("FOPF survival")
        self.clock = pygame.time.Clock()
        self.map = field.Map(50, 20, self.COLLIDER_RESOLUTION)
        self.camera.render_tiles(self.map)
        self.running = False


    def run(self):
        self.running = True
        x = 0
        y = 0
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.WIDTH = event.w
                    self.HEIGHT = event.h
                    self.camera.update_view(self.WIDTH, self.HEIGHT)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                x += -10
            if keys[pygame.K_d]:
                x += 10
            if keys[pygame.K_w]:
                y += -10
            if keys[pygame.K_s]:
                y += 10
            self.camera.marching_squares(self.screen, self.map)
            self.camera.position = (x, y)
            pygame.display.flip()
        pygame.quit()