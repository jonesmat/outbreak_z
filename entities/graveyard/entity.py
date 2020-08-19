import pygame

from entities.game_base import GameEntity
from entities.graveyard.states import GraveyardStateSpawning


class Graveyard(GameEntity):
    """ The graveyard is a zombie spawn point. """

    def __init__(self, game, resource_mgr):
        self.graveyard_image = pygame.image.load('entities/graveyard/graveyard.png').convert_alpha()

        GameEntity.__init__(self, game, 'graveyard', self.graveyard_image, resource_mgr)

        # Create an instance of state
        spawning_state = GraveyardStateSpawning(self, 10, resource_mgr)

        # Add the states to the state machine
        self.brain.add_state(spawning_state)

