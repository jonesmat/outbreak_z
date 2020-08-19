from time import time

from entities.base_entity import State
from entities.zombie.entity import Zombie


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
            zombie = Zombie(self.graveyard.game, self.resource_mgr)
            zombie.location = self.graveyard.location
            zombie.brain.set_state("wandering")

            self.graveyard.game.add_entity(zombie)

            self.next_spawn = time() + self.spawn_rate

    def check_conditions(self):
        pass

    def entry_actions(self):
        self.next_spawn = time()

    def exit_actions(self):
        pass