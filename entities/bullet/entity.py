import pygame

from entities.game_base import GameEntity
import entities.bullet.states as states


class Bullet(GameEntity):
    """ Bullet is fired from the Survivor when attacking. """

    def __init__(self, game, resource_mgr):
        self.bullet_image = pygame.image.load('entities/bullet/bullet.png').convert_alpha()

        GameEntity.__init__(self, game, "bullet", self.bullet_image, resource_mgr)

        # Create an instance of each of the states
        seeking_state = states.BulletStateSeeking(self, self.resource_mgr)

        # Add the states to the state machine
        self.brain.add_state(seeking_state)
        self.zombie_id = None


