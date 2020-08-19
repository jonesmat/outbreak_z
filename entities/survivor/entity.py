import pygame
from pygame.math import Vector2

from entities.game_base import GameEntity
from entities.supplycrate.entity import SupplyCrate

import entities.survivor.states as states



class Survivor(GameEntity):
    """ The survivor entity...  """
    supply_cost = 3

    def __init__(self, game, resource_mgr):

        self.survivor_image = pygame.image.load('entities/survivor/survivor.png').convert_alpha()
        self.survivor_dead_image = pygame.image.load('entities/survivor/survivor_dead.png').convert_alpha()
        self.survivor_hit_image = pygame.image.load('entities/survivor/survivor_hit.png').convert_alpha()

        GameEntity.__init__(self, game, 'survivor', self.survivor_image, resource_mgr)

        # Create an instance of each of the states
        exploring_state = states.SurvivorStateExploring(self)
        attacking_state = states.SurvivorStateAttacking(self, self.resource_mgr)
        evading_state = states.SurvivorStateEvading(self)
        seeking_state = states.SurvivorStateSeeking(self)
        dead_state = states.SurvivorStateDead(self, self.survivor_dead_image)

        # Add the states to the state machine
        self.brain.add_state(exploring_state)
        self.brain.add_state(attacking_state)
        self.brain.add_state(evading_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(dead_state)

        self.health = 10
        self.was_hit = False
        self.ammo = 10
        self.zombie_id = 0

        self.evade_until = None

    def bitten(self):
        """ Damages the survivor and checks for death. """
        self.health -= 1
        self.image = self.survivor_hit_image
        self.was_hit = True
        if self.health <= 0:
            self.brain.set_state('dead')

    def draw(self, surface):
        """ Handles drawing of the entity """
        # Call the draw function of the base class
        GameEntity.draw(self, surface)

        # Update survivor image to his alive image if he has restored health above 0.
        if self.was_hit and self.health > 0:
            self.image = self.survivor_image
            self.was_hit = False

        # Draw caution icon above survivor if he's out of ammo.
        if self.ammo < 1 and self.health > 0:
            x_point, y_point = self.location
            width, height = self.resource_mgr.caution_image.get_size()
            surface.blit(self.resource_mgr.caution_image, (x_point - width / 2, (y_point - height / 2) - 10))

        # Debug drawing of target zombie line.
        if self.debug_mode:
            if self.zombie_id:
                zombie = self.game.get(self.zombie_id)
                if zombie is not None:
                    pygame.draw.line(surface, (25, 100, 255), self.location, zombie.location)
            # blit ammo
            surface.blit(self.resource_mgr.font.render(str(self.ammo), True, (0, 0, 0)), self.location - Vector2(20, 0))
            # blit health
            surface.blit(self.resource_mgr.font.render(str(self.health), True, (0, 0, 0)),
                         self.location - Vector2(5, 22))

