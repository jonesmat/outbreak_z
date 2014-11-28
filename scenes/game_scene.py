""" This is the main game scene where the main game is played (instead of the Title or End Game scene for example).
"""

from random import randint

from pygame.math import Vector2

from game.world import World
from scenes.ui import UI
from entities.graveyard import Graveyard
from entities.survivor import Survivor, Supplies


class GameScene(object):
    def __init__(self, world_size, resources):
        # Inputs
        self.world_size = world_size
        self.resources = resources

        self.world = World(resources, world_size)
        self.ui = UI()

    def generate_world(self):
        self.world.supply = 20

        # Spawn a few graveyards
        for _ in range(1, randint(3, 6)):
            spawn_loc = Vector2(randint(0, self.world_size[0]), randint(0, self.world_size[1]))
            graveyard = Graveyard(self.world, self.resources.graveyard_image, self.resources.zombie_image)
            graveyard.location = Vector2(spawn_loc.x, spawn_loc.y)
            graveyard.brain.set_state("spawning")
            self.world.add_entity(graveyard)

    def tick(self, time_passed):
        self.world.process(time_passed)

    def draw(self, screen, debug_mode):
        self.world.render(screen, self.resources.font, debug_mode)
        self.ui.render(screen, self.resources.font, self.world)

        if debug_mode:
            debug_text = 'Debug: '
            screen.blit(self.resources.font.render(debug_text, True, (0, 0, 0)), (0, 0))

    # ############ MOUSE INPUT MGMT ############### #
    def handle_mouse_left_down(self, mouse_pos):
        self.world.spawn_entity(Survivor, mouse_pos[0], mouse_pos[1])

    def handle_mouse_right_down(self, mouse_pos):
        self.world.spawn_entity(Supplies, mouse_pos[0], mouse_pos[1])
