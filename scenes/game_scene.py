""" This is the main game scene where the main game is played (instead of the Title or End Game scene for example).
"""

from random import randint

from pygame.math import Vector2

from game.world import World
from entities.graveyard import Graveyard
from entities.survivor import Survivor, Supplies


class GameScene(object):
    def __init__(self, world_size, resources):
        # Inputs
        self.world_size = world_size
        self.resources = resources

        self.world = World(resources, world_size)
        self.debugging = False

    def generate_world(self):
        self.world.supply = 20

        # Spawn a few graveyards
        for _ in range(0, 5):
            graveyard = Graveyard(self.world, self.resources.graveyard_image, self.resources.zombie_image)
            graveyard.location = Vector2(randint(0, self.world_size[0]), randint(0, self.world_size[1]))
            graveyard.brain.set_state("spawning")
            self.world.add_entity(graveyard)

    def tick(self, time_passed):
        self.world.tick(time_passed)

    # ############## DRAWING ############## #

    def draw(self, surface):
        self.world.draw(surface, self.resources.font, self.debugging)
        self._draw_ui(surface)

    def _draw_ui(self, surface):
        w_bound, h_bound = self.world.bounds

        zombies = "Zombies: " + str(self.world.get_entity_count("zombie"))
        surface.blit(self.resources.font.render(zombies, True, (0, 0, 0)), Vector2(5, h_bound - 20))

        survivors = "Survivors: " + str(self.world.get_entity_count("survivor"))
        surface.blit(self.resources.font.render(survivors, True, (0, 0, 0)), Vector2(120, h_bound - 20))

        res_str = "Supply Remaining: " + str(int(self.world.supply))
        surface.blit(self.resources.font.render(res_str, True, (0, 0, 0)), Vector2(w_bound - 330, h_bound - 20))

        if self.debugging:
            debug_text = 'Debugging'
            surface.blit(self.resources.font.render(debug_text, True, (0, 0, 0)), (0, 0))

    # ############ MOUSE INPUT MGMT ############### #

    def handle_mouse_left_down(self, mouse_pos):
        self.world.spawn_entity(Survivor, mouse_pos[0], mouse_pos[1])

    def handle_mouse_right_down(self, mouse_pos):
        self.world.spawn_entity(Supplies, mouse_pos[0], mouse_pos[1])
