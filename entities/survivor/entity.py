import pygame
from pygame.math import Vector2

from entities.base_entity import GameEntity
from entities.supplycrate.entity import SupplyCrate

import entities.survivor.states as states


class Survivor(GameEntity):
    """The survivor entity..."""

    SIZE = 1  # meters wide and tall
    BASE_SPEED = 2  # meters/second
    SUPPLY_COST = 3

    def __init__(self, game, resource_mgr):

        self.survivor_image = pygame.image.load("entities/survivor/survivor.png").convert_alpha()
        self.survivor_dead_image = pygame.image.load("entities/survivor/survivor_dead.png").convert_alpha()
        self.survivor_hit_image = pygame.image.load("entities/survivor/survivor_hit.png").convert_alpha()

        GameEntity.__init__(self, game, "survivor", self.survivor_image, resource_mgr)

        self.size = Survivor.SIZE

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
        """Damages the survivor and checks for death."""
        self.health -= 1
        self.image = self.survivor_hit_image
        self.was_hit = True
        if self.health <= 0:
            self.brain.set_state("dead")

    def draw(self, surface):
        """Handles drawing of the entity"""
        # Call the draw function of the base class
        GameEntity.draw(self, surface)

        # Convert the "viewport" coordinates into "Device" coordinates for drawing
        dev_location = self.game.scene.get_dev_vec_from_viewport_vec(self.location)

        # Update survivor image to his alive image if they have recovered.
        if self.was_hit and self.health > 0:
            self.image = self.survivor_image
            self.was_hit = False

        if self.ammo < 1 and self.health > 0:
            self._draw_caution_above_survivor(surface)

        # Debug drawing of target zombie line.
        if self.debug_mode:
            if self.zombie_id:
                zombie = self.game.get(self.zombie_id)
                if zombie is not None:
                    pygame.draw.line(surface, (25, 100, 255), dev_location, zombie.location)

            # blit ammo
            surface.blit(self.resource_mgr.font.render(str(self.ammo), True, (0, 0, 0)), dev_location - Vector2(20, 0))

            # blit health
            surface.blit(
                self.resource_mgr.font.render(str(self.health), True, (0, 0, 0)), dev_location - Vector2(5, 22)
            )

    def _draw_caution_above_survivor(self, surface):
        dev_location = self.game.scene.get_dev_vec_from_viewport_vec(self.location)

        width, height = self.resource_mgr.caution_image.get_size()
        surface.blit(self.resource_mgr.caution_image, (dev_location.x - width / 2, (dev_location.y - height / 2) - 10))
