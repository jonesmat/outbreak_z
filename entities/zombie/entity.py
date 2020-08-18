from random import randint

import pygame
from pygame.math import Vector2

from entities.game_base import GameEntity
import entities.zombie.states as states


class Zombie(GameEntity):
    """ The Zombie entity """

    def __init__(self, world, resource_mgr):
        self.zombie_image = pygame.image.load('entities/zombie/zombie.png').convert_alpha()

        GameEntity.__init__(self, world, 'zombie', self.zombie_image, resource_mgr)

        # Create an instance of state
        wandering_state = states.ZombieStateWandering(self)
        seeking_state = states.ZombieStateSeeking(self)
        feeding_state = states.ZombieStateFeeding(self, resource_mgr)

        # Add the states to the state machine
        self.brain.add_state(wandering_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(feeding_state)

        self.survivor_id = 0
        self.health = 3

    def draw(self, surface):
        """ draws the Zombie class and then any debug graphics  """
        # Call the draw function of the base class
        GameEntity.draw(self, surface)

        # Debug drawing of target survivor line.
        if self.debug_mode:
            if self.survivor_id:
                survivor = self.world.get(self.survivor_id)
                if survivor is not None:
                    pygame.draw.line(surface, (255, 25, 25), self.location,
                                     survivor.location)
            # blit health
            surface.blit(self.resource_mgr.font.render(str(self.health), True, (0, 0, 0)),
                         self.location - Vector2(5, 22))

