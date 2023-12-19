from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
#import main

WIDTH = 800
HEIGHT = 600
FPS = 30
TOKEN_SIZE = 60

pygame.init()
surface = pygame.display.set_mode((600, 400))
running = False
def start_the_game():
    global running
    running = True


def is_True():
    return running
def Main_Menu():
    mainmenu = pygame_menu.Menu('Welcome', 800, 600, theme=themes.THEME_SOLARIZED)
    mainmenu.add.text_input('Name: ', default='username', maxchar=20)
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)
    while running!=True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)

        pygame.display.update()

'''def Pause_Menu():
    pausemenu = pygame_menu.Menu('Paused', 600, 400, theme=themes.THEME_SOLARIZED)
    pausemenu.add.button('Continue', start_the_game)
    pausemenu.add.button('Quit', pygame_menu.events.EXIT)'''