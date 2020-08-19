""" This is the main game scene where the main game is played (instead of the Title or End Game scene for example).
"""

from random import randint

from pygame import Rect
from pygame.math import Vector2
from scenes.base_scene import Scene

from game import Game
from entities.graveyard.entity import Graveyard
from entities.survivor.entity import Survivor
from entities.supplycrate.entity import SupplyCrate


class GameScene(Scene):
    def __init__(self, game_size, resource_mgr):
        super().__init__()
        self.viewport_rect = Rect(0, 0, 1000, 1000)

        # Inputs
        self.game_size = game_size
        self.resource_mgr = resource_mgr

        self.game = Game(resource_mgr, game_size)
        self.debugging = False

    def generate_game(self):
        self.game.supply = 20

        # Spawn a few graveyards
        #for _ in range(1, 5):
        graveyard = Graveyard(self.game, self.resource_mgr)
        graveyard.location = Vector2(randint(0, self.game_size[0]), randint(0, self.game_size[1]))
        graveyard.brain.set_state("spawning")
        self.game.add_entity(graveyard)

    def tick(self, time_passed):
        self.game.tick(time_passed)

    # ############## DRAWING ############## #

    def draw(self, surface):
        self.device_rect = surface.get_rect()

        self.game.draw(surface)
        self._draw_ui(surface)

    def _draw_ui(self, surface):
        w_bound, h_bound = self.game.bounds

        zombies = "Zombies: " + str(self.game.get_entity_count("zombie"))
        surface.blit(self.resource_mgr.font.render(zombies, True, (0, 0, 0)), Vector2(5, h_bound - 20))

        survivors = "Survivors: " + str(self.game.get_entity_count("survivor"))
        surface.blit(self.resource_mgr.font.render(survivors, True, (0, 0, 0)), Vector2(120, h_bound - 20))

        res_str = "Supply Remaining: " + str(int(self.game.supply))
        surface.blit(self.resource_mgr.font.render(res_str, True, (0, 0, 0)), Vector2(w_bound - 330, h_bound - 20))

        if self.debugging:
            debug_text = 'Debugging'
            surface.blit(self.resource_mgr.font.render(debug_text, True, (0, 0, 0)), (0, 0))

    # ############ MOUSE INPUT MGMT ############### #

    def handle_mouse_left_down(self, mouse_pos):
        self.game.spawn_entity(Survivor, mouse_pos[0], mouse_pos[1])

    def handle_mouse_right_down(self, mouse_pos):
        self.game.spawn_entity(SupplyCrate, mouse_pos[0], mouse_pos[1])

    # ############ KEYBOARD INPUT MGMT ############### #

    def handle_tilde_key_down(self):
        """ Tilde key indicates a toggling of the debug mode. """
        self.debugging = not self.debugging
        self.game.set_debug_mode(self.debugging)