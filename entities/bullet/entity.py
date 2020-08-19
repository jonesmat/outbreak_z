import pygame

from entities.base_entity import GameEntity
import entities.bullet.states as states


class Bullet(GameEntity):
    """ Bullet is fired from the Survivor when attacking. """
    SIZE = .2  # meters wide and tall
    BASE_SPEED = 40  # meters/second

    def __init__(self, game, resource_mgr):
        self.bullet_image = pygame.image.load('entities/bullet/bullet.png').convert_alpha()

        GameEntity.__init__(self, game, "bullet", self.bullet_image, resource_mgr)

        self.size = Bullet.SIZE

        # Create an instance of each of the states
        seeking_state = states.BulletStateSeeking(self, self.resource_mgr)

        # Add the states to the state machine
        self.brain.add_state(seeking_state)
        self.zombie_id = None


