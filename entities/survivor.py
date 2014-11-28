""" This module contains the Survivor class and its States. """

from random import randint
from time import time

import pygame
from pygame.math import Vector2

from entities.game_base import GameEntity, State
from entities.bullet import Bullet


class Survivor(GameEntity):
    """ The survivor entity...  """
    supply_cost = 3

    def __init__(self, world, image, dead_image, hit_image, bullet_image, blood_image, caution_image):
        GameEntity.__init__(self, world, 'survivor', image)

        # Create an instance of each of the states
        exploring_state = SurvivorStateExploring(self)
        attacking_state = SurvivorStateAttacking(self)
        evading_state = SurvivorStateEvading(self)
        seeking_state = SurvivorStateSeeking(self)
        dead_state = SurvivorStateDead(self, dead_image)

        # Add the states to the state machine
        self.brain.add_state(exploring_state)
        self.brain.add_state(attacking_state)
        self.brain.add_state(evading_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(dead_state)

        self.alive_image = image
        self.dead_image = dead_image
        self.hit_image = hit_image
        self.bullet_image = bullet_image
        self.blood_image = blood_image
        self.caution_image = caution_image
        self.health = 10
        self.was_hit = False
        self.ammo = 10
        self.zombie_id = 0

        self.evade_until = None

    def bitten(self):
        """ Damages the survivor and checks for death. """
        self.health -= 1
        self.image = self.hit_image
        self.was_hit = True
        if self.health <= 0:
            self.brain.set_state('dead')

    def render(self, surface, font, debug_mode):
        """ Handles rendering of the entity """
        # Call the render function of the base class
        GameEntity.render(self, surface, font, debug_mode)

        # Update survivor image to his alive image if he has restored health above 0.
        if self.was_hit and self.health > 0:
            self.image = self.alive_image
            self.was_hit = False

        # Draw caution icon above survivor if he's out of ammo.
        if self.ammo < 1 and self.health > 0:
            x_point, y_point = self.location
            width, height = self.caution_image.get_size()
            surface.blit(self.caution_image, (x_point - width / 2, (y_point - height / 2) - 10))

        # Debug rendering of target zombie line.
        if debug_mode:
            if self.zombie_id:
                zombie = self.world.get(self.zombie_id)
                if zombie is not None:
                    pygame.draw.line(surface, (25, 100, 255), self.location, zombie.location)
            # blit ammo
            surface.blit(font.render(str(self.ammo), True, (0, 0, 0)), self.location - Vector2(20, 0))
            # blit health
            surface.blit(font.render(str(self.health), True, (0, 0, 0)), self.location - Vector2(5, 22))


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
        zombie = self.survivor.world.get_closest_entity("zombie", self.survivor.location)
        if zombie is not None:
            self.survivor.zombie_id = zombie.id
            return "evading"

        # If there is a nearby pile of supplies, and the survivor is low, 
        # switch to seeking state
        if self.survivor.health < 10 or self.survivor.ammo < 10:
            supplies = self.survivor.world.get_close_entity("supplies", self.survivor.location)
            if supplies is not None:
                self.survivor.supplies_id = supplies.id
                return "seeking"

        return None

    def entry_actions(self):
        # Start with random speed and heading
        self.survivor.speed = 40. + randint(-10, 10)
        self.survivor.destination = self.survivor.get_random_destination()


class SurvivorStateAttacking(State):
    """ Once the survivor has a Zombie target, this state handles the
        targeting and shooting. """

    def __init__(self, survivor):
        # Call the base class constructor to init the State
        State.__init__(self, "attacking")
        # Set the survivor that this State will manipulate
        self.survivor = survivor

    def shoot_zombie(self):
        """ Acquires the zombie, spawns a bullet, and decrements the ammo """
        zombie = self.survivor.world.get(self.survivor.zombie_id)
        if zombie is not None:
            bullet = Bullet(self.survivor.world, self.survivor.bullet_image, self.survivor.blood_image)
            bullet.location = self.survivor.location
            bullet.zombie_id = zombie.id
            bullet.brain.set_state("seeking")

            self.survivor.world.add_entity(bullet)
            self.survivor.ammo -= 1

    def do_actions(self):
        # Occasionally take a shot at a zombie if ammo permits.
        if self.survivor.ammo > 0 and randint(1, 30) == 1:
            self.shoot_zombie()

    def check_conditions(self):
        # If there isn't a nearby zombie, switch to exploring state
        zombie = self.survivor.world.get_closest_entity("zombie", self.survivor.location)
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
    """ Handles the survivor evading a zombie thats gotten too close. """

    def __init__(self, survivor):
        # Call the base class constructor to init the State
        State.__init__(self, "evading")
        # Set the survivor that this State will manipulate
        self.survivor = survivor

    def run_away(self):
        """ Determines where the zombie is, then sets the destination for an
            area in the opposite direction. """
        # Try to first find a zombie that isn't feeding, its a lesser threat.
        zombie = self.survivor.world.get_close_entity_in_state("zombie", ["wandering", "seeking"],
                                                               self.survivor.location, 115)
        # If you can't find a non-feeding zombie to run from, see if a 
        # feeding one is close.
        if zombie is None:
            zombie = self.survivor.world.get_close_entity("zombie", self.survivor.location, 115)

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
            w_bound, h_bound = self.survivor.world.bounds
            x_point = abs(min([vec_away.x + randint(-20, 20), w_bound - 5]))
            y_point = abs(min([vec_away.y + randint(-20, 20), h_bound - 5]))
            self.survivor.destination = Vector2(x_point, y_point)

    def do_actions(self):
        # Occasionally make sure another zombie isn't closer.
        if randint(1, 10) == 1:
            self.run_away()

    def check_conditions(self):
        if self.survivor.evade_until is None:
            # Attack a near zombie if we have ammo.
            zombie = self.survivor.world.get_close_entity("zombie", self.survivor.location)
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
        zombie = self.survivor.world.get(self.survivor.zombie_id)
        if zombie is not None:
            self.survivor.speed = 70. + randint(-10, 10)
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
        zombie = self.survivor.world.get_closest_entity("zombie",
                                                        self.survivor.location)
        if zombie is not None:
            self.survivor.zombie_id = zombie.id
            return "evading"

        # If the supplies are gone, go back to exploring
        supplies = self.survivor.world.get(self.survivor.supplies_id)
        if supplies is None:
            return "exploring"

        # If we are next to the supplies, pick them up.
        if self.survivor.location.distance_to(supplies.location) < 5.0:
            self.survivor.world.remove_entity(supplies)
            self.survivor.ammo = 10
            self.survivor.health = 10
            return "exploring"

        return None

    def entry_actions(self):
        # Target the supplies.
        supplies = self.survivor.world.get(self.survivor.supplies_id)
        if supplies is not None:
            self.survivor.destination = supplies.location


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

        return None

    def entry_actions(self):
        self.survivor.speed = 0
        self.survivor.image = self.dead_image


class Supplies(GameEntity):
    supply_cost = 1

    """ Simple supply entity """

    def __init__(self, world, image):
        GameEntity.__init__(self, world, "supplies", image, draw_priority=6)