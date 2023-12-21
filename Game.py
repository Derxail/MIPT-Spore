import math
import random

import pygame

import UI
import field
import frontend
import entities

import pygame_menu
from pygame_menu import themes

import utils


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 30
        self.GRID_W = 50
        self.GRID_H = 30
        self.TOKEN_SIZE = 70
        self.TILE_SIZE = int(self.TOKEN_SIZE * 2)
        self.COLLIDER_RESOLUTION = 300
        self.PLAYER_SIZE = self.TOKEN_SIZE * 1.0
        self.ENEMIES_CNT = 15
        self.ENEMIES_SPAWN_PERIOD = 0.35
        self.SPAWN_POINTS_CNT = 20
        self.PLAYER_IMAGE = pygame.image.load('images\\Player.png')
        self.PLAYER_IMAGE = pygame.transform.scale(
            self.PLAYER_IMAGE,
            (self.PLAYER_SIZE,
            self.PLAYER_SIZE)
        )
        self.PROJECTILE_IMAGE = pygame.image.load('images\\Axe.png')
        self.PROJECTILE_IMAGE = pygame.transform.scale(
            self.PROJECTILE_IMAGE,
            (self.TOKEN_SIZE,
             self.TOKEN_SIZE)
        )
        self.SCALE_FACTOR = self.TILE_SIZE / self.COLLIDER_RESOLUTION
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
        self.map = field.Map(
            self.GRID_W,
            self.GRID_H,
            self.COLLIDER_RESOLUTION,
            self.SCALE_FACTOR,
            spawn_points_cnt=self.SPAWN_POINTS_CNT
        )
        print(self.map.get_spawn_points())
        self.map.write_object(self.player)
        self.camera.render_tiles(self.map)
        self.paused = False
        self.running = False
        self.pause_text = pause_text = pygame.font.SysFont('Consolas', 32).render('Ok, nigga we\'ll wait', True, pygame.color.Color('White'))
        self.xp_bar = UI.HealthBar(
            value=0,
            max_value=10,
            length=self.WIDTH*0.85,
            height=30,
            color=(30, 255, 0),
            outline_thickness=3
        )

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

    def draw_ui(self):
        self.screen.blit(self.xp_bar.surface, (0.075*self.WIDTH, 20))

    def camera_follow(self):
        self.camera.position = (self.player.position[1] * self.SCALE_FACTOR, self.player.position[0] * self.SCALE_FACTOR)

    def on_enemy_kill_by_player(self):
        value = self.xp_bar.value
        max_value = self.xp_bar.max_value
        if value + 1 >= max_value:
            self.xp_bar.set_max_value(max_value + 5)
            self.xp_bar.set_value(0)
        else:
            self.xp_bar.set_value(value + 2)

    def spawn_enemy(self):
        if(len(self.enemies) >= self.ENEMIES_CNT):
            return
        spawn_points = self.map.get_spawn_points()
        point = spawn_points[random.randint(0, self.SPAWN_POINTS_CNT - 1)]

        #СПАСИ И СОХРАНИ!---------------------------------------
        if (point[0] >= 0.85*self.COLLIDER_RESOLUTION*self.GRID_H
            or point[1] >= 0.85*self.COLLIDER_RESOLUTION*self.GRID_W):
            return
        #-------------------------------------------------------

        enemy = entities.Creature(
            coords=point,
            image=self.PLAYER_IMAGE,
            collider_resolution=self.COLLIDER_RESOLUTION / 2,
            hp=random.randint(2, 10)
        )
        self.enemies.append(enemy)
        self.map.write_object(enemy)

    def launch_projectile(
            self,
            initial_pos,
            v,
            angle
    ):
        projectile = entities.Projectile(
            initial_pos.copy(),
            self.PROJECTILE_IMAGE,
            self.COLLIDER_RESOLUTION // 10,
            v * math.cos(angle),
            v * math.sin(angle),
            id(self.player),
            player_id=id(self.player),
            kill_callback=self.on_enemy_kill_by_player,
            ang_speed=9
        )
        self.projectiles.append(projectile)
        self.map.write_object(projectile)

    def run(self):

        self.main_menu_callup()
        self.start_the_game()
        enemy_spawn_timer = 0.0

        while self.running:
            vx = 0
            vy = 0
            # dt - в секундах
            dt = self.clock.tick(self.FPS) / 1000

            enemy_spawn_timer += dt
            if enemy_spawn_timer > self.ENEMIES_SPAWN_PERIOD:
                self.spawn_enemy()
                enemy_spawn_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.WIDTH = event.w
                    self.HEIGHT = event.h
                    self.camera.update_view(self.WIDTH, self.HEIGHT)
                elif event.type == pygame.MOUSEMOTION:
                    self.player.angle = utils.angle_by_coords(
                        pos0=event.pos,
                        pos=(self.camera.view_size[0] / 2 + self.PLAYER_SIZE/2,
                             self.camera.view_size[1] / 2 + self.PLAYER_SIZE/2
                        )
                    )
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.launch_projectile(self.player.position, 1000, self.player.angle)


            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                vx = -1000
            if keys[pygame.K_d]:
                vx = 1000
            if keys[pygame.K_w]:
                vy = -1000
            if keys[pygame.K_s]:
                vy = 1000
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
            self.player.set_speed(vx, vy)

            for enemy in self.enemies:
                enemy.update(self.map, dt)

            self.player.update(self.map, dt)

            ind = 0
            while ind < len(self.projectiles):
                projectile = self.projectiles[ind]
                projectile.update(self.map, dt)
                if not projectile.flies:
                    self.projectiles.remove(projectile)
                    self.map.remove_object(projectile)
                else:
                    projectile.move(self.map, dt)
                    ind += 1

            self.player.move(self.map, dt)
            ind = 0
            while ind < len(self.enemies):
                enemy = self.enemies[ind]
                if not enemy.alive:
                    self.enemies.remove(enemy)
                    self.map.remove_object(enemy)
                else:
                    enemy.move(self.map, dt)
                    ind += 1

            self.map.update(dt)
            self.camera_follow()
            self.camera.marching_squares(self.screen, self.map)
            self.draw_ui()
            pygame.display.flip()

        pygame.quit()