""" This module contains the Graveyard Class """

from time import time

from entities.game_base import GameEntity, State
from entities.zombie import Zombie


class Graveyard(GameEntity):
    """ The graveyard is a zombie spawn point. """

    def __init__(self, world, resource_mgr):
        GameEntity.__init__(self, world, 'graveyard', resource_mgr.graveyard_image, resource_mgr)

        # Create an instance of state
        spawning_state = GraveyardStateSpawning(self, 10, resource_mgr)

        # Add the states to the state machine
        self.brain.add_state(spawning_state)


class GraveyardStateSpawning(State):
    def __init__(self, graveyard, spawn_rate, resource_mgr):
        # Call the base class constructor to init the State
        State.__init__(self, "spawning")

        # Set the entity that this State will manipulate
        self.graveyard = graveyard

        self.spawn_rate = spawn_rate
        self.resource_mgr = resource_mgr
        self.next_spawn = None

    def do_actions(self):
        if time() > self.next_spawn:
            zombie = Zombie(self.graveyard.world, self.resource_mgr)
            zombie.location = self.graveyard.location
            zombie.brain.set_state("wandering")

            self.graveyard.world.add_entity(zombie)

            self.next_spawn = time() + self.spawn_rate

    def check_conditions(self):
        pass

    def entry_actions(self):
        self.next_spawn = time()

    def exit_actions(self):
        pass