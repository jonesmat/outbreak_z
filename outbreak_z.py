from sys import exit

import pygame
from pygame.locals import QUIT, KEYDOWN, K_q, K_ESCAPE, K_BACKQUOTE, MOUSEBUTTONDOWN

from resources.resources import Resources
from scenes.game_scene import GameScene


pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

debug_mode = False

resources = Resources()
resources.font = pygame.font.SysFont("arial", 16)

active_scene = GameScene(SCREEN_SIZE, resources)

active_scene.generate_world()

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE:
                exit()
            if event.key == K_BACKQUOTE:
                debug_mode = not debug_mode
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                active_scene.handle_mouse_left_down(pygame.mouse.get_pos())
            if event.button == 3:
                active_scene.handle_mouse_right_down(pygame.mouse.get_pos())

    time_passed = clock.tick(30)

    active_scene.tick(time_passed)
    active_scene.draw(screen, debug_mode)

    pygame.display.update()

