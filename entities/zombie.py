""" Module contains the Zombie class """

from random import randint

import pygame
from pygame.math import Vector2

from entities.game_base import GameEntity, State


class Zombie(GameEntity):
    """ The Zombie entity """

    def __init__(self, world, image):
        GameEntity.__init__(self, world, 'zombie', image)

        # Create an instance of state
        wandering_state = ZombieStateWandering(self)
        seeking_state = ZombieStateSeeking(self)
        feeding_state = ZombieStateFeeding(self)

        # Add the states to the state machine
        self.brain.add_state(wandering_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(feeding_state)

        self.survivor_id = 0
        self.health = 3

    def draw(self, surface, font, debug_mode):
        """ draws the Zombie class and then any debug graphics  """
        # Call the draw function of the base class
        GameEntity.draw(self, surface, font, debug_mode)

        # Debug drawing of target survivor line.
        if debug_mode:
            if self.survivor_id:
                survivor = self.world.get(self.survivor_id)
                if survivor is not None:
                    pygame.draw.line(surface, (255, 25, 25), self.location,
                                     survivor.location)
            # blit health
            surface.blit(font.render(str(self.health), True, (0, 0, 0)),
                         self.location - Vector2(5, 22))


class ZombieStateWandering(State):
    """ The default state for a Zombie, wandering aimlessly """

    def __init__(self, zombie):
        # Call the base class constructor to init the State
        State.__init__(self, "wandering")
        # Set the Zombie that this State will manipulate
        self.zombie = zombie

    def do_actions(self):
        # Change direction occasionally
        if randint(1, 350) == 1 or \
                        self.zombie.location == self.zombie.destination:
            self.zombie.destination = self.zombie.get_random_destination()

    def check_conditions(self):
        # If there is a nearby dead survivor, switch to eating state
        survivor = self.zombie.world.get_close_entity_in_state("survivor",
                                                               ["dead"], self.zombie.location, 15.)
        if survivor is not None:
            self.zombie.survivor_id = survivor.id
            return "feeding"

        # If there is a nearby survivor, switch to seeking state
        survivor = self.zombie.world.get_close_entity("survivor",
                                                      self.zombie.location)
        if survivor is not None:
            self.zombie.survivor_id = survivor.id
            return "seeking"

        return None

    def entry_actions(self):
        # Start with random speed and heading
        self.zombie.speed = 15. + randint(-3, 3)
        self.zombie.destination = self.zombie.get_random_destination()


class ZombieStateSeeking(State):
    """ Once the zombie has a target, this State guides him to his target """

    def __init__(self, zombie):
        State.__init__(self, "seeking")
        self.zombie = zombie

    def do_actions(self):
        # Keep the closes survivor as the target.
        survivor = self.zombie.world.get_closest_entity("survivor",
                                                        self.zombie.location)
        if survivor is not None:
            self.zombie.survivor_id = survivor.id
            self.zombie.destination = survivor.location

    def check_conditions(self):
        # If no survivor in range, wander
        survivor = self.zombie.world.get_closest_entity("survivor",
                                                        self.zombie.location, 115)
        if survivor is None:
            self.zombie.survivor_id = 0
            return "wandering"

        # If the zombie is close enough to the survivor, attempt to kill it.
        if self.zombie.location.distance_to(survivor.location) <= 15.:
            # Give the survivor a fighting chance to avoid being killed!
            if randint(1, 5) == 1:
                survivor.bitten()

            # If the survivor is dead, start feeding.
            if survivor.health <= 0:
                return "feeding"

    def entry_actions(self):
        # Start seeking with a quickend pace.
        self.zombie.speed = 30. + randint(-15, 15)


class ZombieStateFeeding(State):
    """ The Feeding state handles eating a downed survivor. """

    def __init__(self, zombie):
        # Call the base class constructor to init the State
        State.__init__(self, "feeding")
        # Set the Zombie that this State will manipulate
        self.zombie = zombie

    def do_actions(self):
        # Bit the survivor
        survivor = self.zombie.world.get(self.zombie.survivor_id)
        if survivor is not None:
            survivor.bitten()

    def check_conditions(self):
        # If survivor is consumed, start wandering
        survivor = self.zombie.world.get(self.zombie.survivor_id)
        if survivor is not None:
            if survivor.health <= -200:
                # Survivor is now consumed
                self.zombie.world.remove_entity(survivor)

                # Replace the survivor with a new zombie.
                new_zombie = Zombie(self.zombie.world, self.zombie.image)
                new_zombie.location = Vector2(survivor.location.x,
                                              survivor.location.y)
                new_zombie.brain.set_state("wandering")
                self.zombie.world.add_entity(new_zombie)

                self.zombie.survivor_id = 0
                return "wandering"

        # if no dead survivor is nearby, start wandering
        survivor = self.zombie.world.get_close_entity_in_state("survivor",
                                                               ["dead"], self.zombie.location, 15.)
        if survivor is None:
            self.zombie.survivor_id = 0
            return "wandering"

        return None

    def entry_actions(self):
        # Start with random speed and heading
        self.zombie.speed = 0
