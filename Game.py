import math

import pygame
import field
import frontend
import entities

import pygame_menu
from pygame_menu import themes

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 30
        self.TOKEN_SIZE = 60
        self.TILE_SIZE = int(self.TOKEN_SIZE * 2)
        self.COLLIDER_RESOLUTION = 300
        self.PLAYER_IMAGE = pygame.Surface([self.TOKEN_SIZE, self.TOKEN_SIZE], pygame.SRCALPHA)
        self.SCALE_FACTOR = self.TILE_SIZE / self.COLLIDER_RESOLUTION
        pygame.draw.circle(
            self.PLAYER_IMAGE, (9, 158, 160), (self.TOKEN_SIZE / 2, self.TOKEN_SIZE / 2), self.TOKEN_SIZE / 2
        )
        self.enemies = []
        self.projectiles = []
        self.player = entities.Creature(
            [100, 100], self.PLAYER_IMAGE, self.COLLIDER_RESOLUTION / 2
        )
        self.camera = frontend.Camera(
            self.player.position, (self.WIDTH, self.HEIGHT), self.TILE_SIZE
        )
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("FOPF survival")
        self.clock = pygame.time.Clock()
        self.map = field.Map(50, 30, self.COLLIDER_RESOLUTION)
        self.map.write_object(self.player)
        self.camera.render_tiles(self.map)
        self.paused = False
        self.running = False
        self.pause_text = pause_text = pygame.font.SysFont('Consolas', 32).render('Ok, nigga we\'ll wait', True, pygame.color.Color('White'))

    def start_the_game(self):
        self.running=True

    def main_menu_callup(self):
        mainmenu = pygame_menu.Menu('Welcome', 800, 600, theme=themes.THEME_SOLARIZED)
        mainmenu.add.text_input('Name: ', default='username', maxchar=20)
        mainmenu.add.button('Play', self.start_the_game)
        mainmenu.add.button('Quit', pygame_menu.events.EXIT)
        while self.running != True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if mainmenu.is_enabled():
                mainmenu.update(events)
                mainmenu.draw(self.screen)

            pygame.display.update()

    def pause_menu_callup(self):
        pass
    def camera_follow(self):
        self.camera.position = (self.player.position[1] * self.SCALE_FACTOR, self.player.position[0] * self.SCALE_FACTOR)

    def run(self):
        self.main_menu_callup()
        self.running = True
        x = 0
        y = 0
        while self.running:
            vx = 0
            vy = 0
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.WIDTH = event.w
                    self.HEIGHT = event.h
                    self.camera.update_view(self.WIDTH, self.HEIGHT)
                elif event.type == pygame.MOUSEMOTION:
                    self.player.targetting(event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.projectiles.append(entities.Projectile(self.player.position, self.PLAYER_IMAGE, self.COLLIDER_RESOLUTION // 10, 30 * math.cos(self.player.angle), 30 * math.sin(self.player.angle)))


            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                vx = -30
            if keys[pygame.K_d]:
                vx = 30
            if keys[pygame.K_w]:
                vy = -30
            if keys[pygame.K_s]:
                vy = 30
            if keys[pygame.K_ESCAPE]:
                if self.paused == True:
                    self.pause=False
                else:
                    self.paused = True
                if self.paused:
                    self.pause_menu_callup()
                    self.screen.blit(self.pause_text, (100, 100))

            if vx != 0 and vy != 0:
                vx = int(vx / 1.41)
                vy = int(vy / 1.41)

            ind = 0
            while ind < len(self.projectiles):
                projectile = self.projectiles[ind]
                if not projectile.flies:
                    del projectile
                    del self.projectiles[ind]
                else:
                    projectile.move(self.map)
                    ind += 1

            self.camera.marching_squares(self.screen, self.map)
            self.player.move(self.map, vy, vx)
            self.camera_follow()


            pygame.display.flip()
        pygame.quit()