import pygame
from pygame.locals import QUIT, KEYDOWN, K_q, K_ESCAPE, K_BACKQUOTE, MOUSEBUTTONDOWN

from resources.resourcemgr import ResourceMgr
from scenes.game_scene import GameScene


def main():
    pygame.init()
    SCREEN_SIZE = (800, 600)
    surface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    clock = pygame.time.Clock()

    active_scene = GameScene(SCREEN_SIZE, ResourceMgr())
    active_scene.generate_game()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_q or event.key == K_ESCAPE:
                    return
                if event.key == K_BACKQUOTE:
                    active_scene.handle_tilde_key_down()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    active_scene.handle_mouse_left_down(pygame.mouse.get_pos())
                if event.button == 3:
                    active_scene.handle_mouse_right_down(pygame.mouse.get_pos())

        time_passed = clock.tick(30)

        active_scene.tick(time_passed)
        active_scene.draw(surface)

        pygame.display.update()


main()