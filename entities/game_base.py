"""
    game_base contains base and misc classes used by outbreak-z.
"""

from random import randint
from uuid import uuid1 as uuid

from pygame.math import Vector2


class GameEntity(object):
    """ The base object for any entity that will exist inside the game
        world.  This class handles the drawing and processing each tick. """

    def __init__(self, world, name, image, draw_priority=10):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.

        self.brain = StateMachine()

        self.entity_id = str(uuid())

        self.prev_destination = None
        self.redirect_timer = None

        self.draw_priority = draw_priority

    def __str__(self):
        return self.name + ':' + str(self.entity_id) + ' - ' + self.brain.active_state.name

    def draw(self, surface, font, debug_mode):
        """ Draws the entities image centered (horz and vert) on its
            current location. """
        x_point, y_point = self.location
        width, height = self.image.get_size()
        surface.blit(self.image, (x_point - width / 2, y_point - height / 2))

        if debug_mode:
            if self.brain is not None and self.brain.active_state is not None:
                debug_letter = self.brain.active_state.name[:2]
                if len(debug_letter) == 2:
                    surface.blit(font.render(debug_letter, True, (0, 0, 0)),
                                 self.location)

    def tick(self, time_passed):
        """ Triggers the entities StateMachine and locomotion """
        self.brain.think()
        if self.speed > 0 and self.location != self.destination:
            self._check_collisions_(time_passed)
            self._move_(time_passed)

    def get_random_destination(self):
        """ Returns a random vector within the world bounds """
        width, height = self.world.bounds
        return Vector2(randint(0, width), randint(0, height))

    def _check_collisions_(self, time_passed):
        """ Checks to see if the entities current location is too close
            to another entity, if so, randomly changes the destination
            for the next second."""
        if self.redirect_timer is None:
            # Check to make sure the entity isn't too close to another.
            collision_distance = 2
            blocking_entity = self.world.get_close_entity(None, self.location, collision_distance, self.entity_id)

            if blocking_entity is not None:
                self.prev_destination = self.destination
                self.destination = self.get_random_destination()
                self.redirect_timer = 1000  # 1 second
        else:
            if self.redirect_timer > 0:
                # Currently redirecting, decrement timer by time passed
                self.redirect_timer -= time_passed
            else:
                # redirecting time expired, reset destination
                self.destination = self.prev_destination
                self.prev_destination = None
                self.redirect_timer = None

    def _move_(self, time_passed):
        """ Provides locomotion for the entity while ensuring it stays
            within the world bounds. """
        vec_to_destination = self.destination - self.location
        distance_to_destination = vec_to_destination.length()
        heading = vec_to_destination.normalize()
        travel_distance = min(distance_to_destination, time_passed * self.speed)
        self.location = self.location + travel_distance * heading

        # Ensure the entity stays within the boundaries:
        if self.location.x < 0:
            self.location.x = 0
        if self.location.x > self.world.bounds[0]:
            self.location.x = self.world.bounds[0]
        if self.location.y < 0:
            self.location.y = 0
        if self.location.y > self.world.bounds[1]:
            self.location.y = self.world.bounds[1]


class State(object):
    """ Interface class for all State objects. """

    def __init__(self, name):
        self.name = name

    def entry_actions(self):
        """ Override this method with any actions that are to be preformed
            when this state begins. """
        pass

    def do_actions(self):
        """ Override this method with any actions you want to be preformed
            every tick."""
        pass

    def check_conditions(self):
        """ Override this method with conditional checks for leaving this
            state. """
        pass

    def exit_actions(self):
        """ Override this method with any actions that are to be preformed
            as this state is exiting. """
        pass


class StateMachine(object):
    """ As the brains of each GameEntity, the StateMachine manages the
        States provided to it and their execution. """

    def __init__(self):
        self.states = {}  # Stores the states
        self.active_state = None  # The currently active state

    def add_state(self, state):
        """ Add a state to the internal dictionary """
        self.states[state.name] = state

    def think(self):
        """ Perform the actions of the active state and check conditions """
        # Only continue if there is an active state
        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        """ Change states and perform  any exit / entry actions """
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()
