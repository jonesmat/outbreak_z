from random import randint
from time import time

from pygame.math import Vector2

from entities.game_base import State
from entities.bullet.entity import Bullet


class SurvivorStateExploring(State):
    """ Exploring is the default survivor state when the entity
        wanders around looking for supplies """

    def __init__(self, survivor):
        # Call the base class constructor to init the State
        State.__init__(self, "exploring")
        # Set the survivor that this State will manipulate
        self.survivor = survivor

    def do_actions(self):
        # Change direction occasionally
        if randint(1, 200) == 1 or self.survivor.location == self.survivor.destination:
            self.survivor.destination = self.survivor.get_random_destination()

    def check_conditions(self):
        # If there is a nearby zombie...
        zombie = self.survivor.game.get_closest_entity("zombie", self.survivor.location)
        if zombie is not None:
            self.survivor.zombie_id = zombie.id
            return "evading"

        # If there is a nearby pile of supplies, and the survivor is low, 
        # switch to seeking state
        if self.survivor.health < 10 or self.survivor.ammo < 10:
            supplycrate = self.survivor.game.get_close_entity("supplycrate", self.survivor.location)
            if supplycrate is not None:
                self.survivor.supplies_id = supplycrate.id
                return "seeking"

        return None

    def entry_actions(self):
        # Start with random speed and heading
        self.survivor.speed = self.survivor.BASE_SPEED
        self.survivor.destination = self.survivor.get_random_destination()


class SurvivorStateAttacking(State):
    """ Once the survivor has a Zombie target, this state handles the
        targeting and shooting. """

    def __init__(self, survivor, resource_mgr):
        # Call the base class constructor to init the State
        State.__init__(self, "attacking")
        # Set the survivor that this State will manipulate
        self.survivor = survivor
        self.resource_mgr = resource_mgr

    def shoot_zombie(self):
        """ Acquires the zombie, spawns a bullet, and decrements the ammo """
        zombie = self.survivor.game.get(self.survivor.zombie_id)
        if zombie is not None:
            bullet = Bullet(self.survivor.game, self.resource_mgr)
            bullet.location = self.survivor.location
            bullet.zombie_id = zombie.id
            bullet.brain.set_state("seeking")

            self.survivor.game.add_entity(bullet)
            self.survivor.ammo -= 1

    def do_actions(self):
        # Occasionally take a shot at a zombie if ammo permits.
        if self.survivor.ammo > 0 and randint(1, 30) == 1:
            self.shoot_zombie()

    def check_conditions(self):
        # If there isn't a nearby zombie, switch to exploring state
        zombie = self.survivor.game.get_closest_entity("zombie", self.survivor.location)
        if zombie is None:
            self.survivor.zombie_id = None
            return "exploring"

        # If there is a zombie nearby, switch to that target.
        self.survivor.zombie_id = zombie.id

        # If the survivor is out of ammo, switch to evading.
        if self.survivor.ammo <= 0:
            return "evading"

        # Roughly after a second the survivor should stop shooting and
        # attempt to evade for 2 seconds
        if randint(1, 50) == 1:
            self.survivor.evade_until = time() + 2  # 2 seconds from now
            return "evading"

        return None

    def entry_actions(self):
        # Stop moving to fire
        self.survivor.destination = self.survivor.location


class SurvivorStateEvading(State):
    """ Handles the survivor evading a zombie that's gotten too close. """

    def __init__(self, survivor):
        # Call the base class constructor to init the State
        State.__init__(self, "evading")
        # Set the survivor that this State will manipulate
        self.survivor = survivor

    def do_actions(self):
        # Occasionally make sure another zombie isn't closer.
        if randint(1, 10) == 1:
            self.choose_new_evade_target()

    def choose_new_evade_target(self):
        """ Determines where the zombie is, then sets the destination for an
            area in the opposite direction. """
        # Try to first find a zombie that isn't feeding, its a lesser threat.
        zombie = self.survivor.game.get_close_entity_in_state("zombie", ["wandering", "seeking"], self.survivor.location, 25)
        
        # If you can't find a non-feeding zombie to run from, see if a feeding one is close.
        if zombie is None:
            zombie = self.survivor.game.get_close_entity("zombie", self.survivor.location, 25)

        # If one is found, RUN!
        if zombie is not None:
            self.survivor.zombie_id = zombie.id

            # In order to point our destination away from the zombie, we
            # must get the vector to the zombie...
            vec_to_zombie = zombie.location - self.survivor.location
            # ... then subtract that zombie from our current location to
            # go in the opposite direction.
            vec_away = self.survivor.location - vec_to_zombie
            # Set the destination as a slightly random vector away that isn't
            # negative and also stays a bit away from the max screen size.
            w_bound = self.survivor.game.scene.viewport_rect.right
            h_bound = self.survivor.game.scene.viewport_rect.bottom

            x_point = abs(min([vec_away.x + randint(-20, 20), w_bound - 5]))
            y_point = abs(min([vec_away.y + randint(-20, 20), h_bound - 5]))
            self.survivor.destination = Vector2(x_point, y_point)

    def check_conditions(self):
        if self.survivor.evade_until is None:
            # Attack a near zombie if we have ammo.
            zombie = self.survivor.game.get_close_entity("zombie", self.survivor.location)
            if zombie is not None and self.survivor.ammo > 0:
                return "attacking"

            # If there isn't a nearby zombie, switch to exploring state
            if zombie is None:
                self.survivor.zombie_id = None
                return "exploring"
        elif self.survivor.evade_until < time():
            # evade_until timer elapsed, clear it
            self.survivor.evade_until = None

        return None

    def entry_actions(self):
        # Start with hightend speed with heading away from zombie.
        zombie = self.survivor.game.get(self.survivor.zombie_id)
        if zombie is not None:
            self.survivor.speed = self.survivor.BASE_SPEED * 2
            self.survivor.destination = -zombie.location


class SurvivorStateSeeking(State):
    """ Once the survivor has spotted a supply crate, this state handles
        the entity making his way over to collect """

    def __init__(self, survivor):
        # Call the base class constructor to init the State
        State.__init__(self, "seeking")
        # Set the survivor that this State will manipulate
        self.survivor = survivor
        self.supplies_id = None

    def check_conditions(self):
        # If there is a nearby zombie...
        zombie = self.survivor.game.get_closest_entity("zombie", self.survivor.location)
        if zombie is not None:
            self.survivor.zombie_id = zombie.id
            return "evading"

        # If the supplies are gone, go back to exploring
        supplycrate = self.survivor.game.get(self.survivor.supplies_id)
        if supplycrate is None:
            return "exploring"

        # If we are next to the supplies, pick them up.
        if self.survivor.location.distance_to(supplycrate.location) < 1.0:
            self.survivor.game.remove_entity(supplycrate)
            self.survivor.ammo = 10
            self.survivor.health = 10
            return "exploring"

        return None

    def entry_actions(self):
        # Target the supplies.
        supplycrate = self.survivor.game.get(self.survivor.supplies_id)
        if supplycrate is not None:
            self.survivor.destination = supplycrate.location


class SurvivorStateDead(State):
    """ Once the survivor is down (dead) he becomes zombie food.  In the
        off chance that another survivor helps the entity, he can return
        to exploring. """

    def __init__(self, survivor, dead_image):
        # Call the base class constructor to init the State
        State.__init__(self, "dead")
        # Set the survivor that this State will manipulate
        self.survivor = survivor
        self.dead_image = dead_image

    def do_actions(self):
        if randint(1, 10) == 1:
            self.survivor.health += 5

    def check_conditions(self):
        if self.survivor.health >= 10:
            return "exploring"
        
        elif self.survivor.health <= -200:
            self.survivor.game.turn_survivor(self.survivor)

        return None

    def entry_actions(self):
        self.survivor.speed = 0
        self.survivor.image = self.dead_image
