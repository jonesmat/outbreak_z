from random import randint

import pygame
from pygame.math import Vector2

from entities.base_entity import GameEntity, State


class ZombieStateWandering(State):
    """ The default state for a Zombie, wandering aimlessly """

    def __init__(self, zombie):
        # Call the base class constructor to init the State
        State.__init__(self, "wandering")
        # Set the Zombie that this State will manipulate
        self.zombie = zombie

    def do_actions(self):
        # Change direction occasionally
        if randint(1, 350) == 1 or self.zombie.location == self.zombie.destination:
            self.zombie.destination = self.zombie.get_random_destination()

    def check_conditions(self):
        # If there is a nearby dead survivor, switch to eating state
        survivor = self.zombie.game.get_close_entity_in_state("survivor", ["dead"], self.zombie.location, 2.)
        if survivor is not None:
            self.zombie.survivor_id = survivor.id
            return "feeding"

        # If there is a nearby survivor, switch to seeking state
        survivor = self.zombie.game.get_close_entity("survivor",
                                                      self.zombie.location)
        if survivor is not None:
            self.zombie.survivor_id = survivor.id
            return "seeking"

        return None

    def entry_actions(self):
        # Start with random speed and heading
        self.zombie.speed = self.zombie.BASE_SPEED / 2
        self.zombie.destination = self.zombie.get_random_destination()


class ZombieStateSeeking(State):
    """ Once the zombie has a target, this State guides him to his target """

    def __init__(self, zombie):
        State.__init__(self, "seeking")
        self.zombie = zombie

    def do_actions(self):
        # Keep the closes survivor as the target.
        survivor = self.zombie.game.get_closest_entity("survivor",
                                                        self.zombie.location)
        if survivor is not None:
            self.zombie.survivor_id = survivor.id
            self.zombie.destination = survivor.location

    def check_conditions(self):
        # If no survivor in range, wander
        survivor = self.zombie.game.get_closest_entity("survivor",
                                                        self.zombie.location, 25)
        if survivor is None:
            self.zombie.survivor_id = 0
            return "wandering"

        # If the zombie is close enough to the survivor, attempt to kill it.
        if self.zombie.location.distance_to(survivor.location) <= 3.:
            # Give the survivor a fighting chance to avoid being killed!
            if randint(1, 5) == 1:
                survivor.bitten()

            # If the survivor is dead, start feeding.
            if survivor.health <= 0:
                return "feeding"

    def entry_actions(self):
        # Start seeking with a quickend pace.
        self.zombie.speed = self.zombie.BASE_SPEED


class ZombieStateFeeding(State):
    """ The Feeding state handles eating a downed survivor. """

    def __init__(self, zombie, resource_mgr):
        # Call the base class constructor to init the State
        State.__init__(self, "feeding")
        # Set the Zombie that this State will manipulate
        self.zombie = zombie
        self.resource_mgr = resource_mgr

    def do_actions(self):
        # Bit the survivor
        survivor = self.zombie.game.get(self.zombie.survivor_id)
        if survivor is not None:
            survivor.bitten()

    def check_conditions(self):
        # if no dead survivor is nearby, start wandering
        survivor = self.zombie.game.get_close_entity_in_state("survivor", ["dead"], self.zombie.location, 2.)
        if survivor is None:
            self.zombie.survivor_id = 0
            return "wandering"

        return None

    def entry_actions(self):
        # Start with random speed and heading
        self.zombie.speed = 0
