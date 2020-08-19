"""
    game_base contains base and misc classes used by outbreak-z.
"""

from random import randint
from uuid import uuid1 as uuid

from pygame.math import Vector2


class GameEntity(object):
    """ The base object for any entity that will exist inside the game
        game.  This class handles the drawing and processing each tick. """

    def __init__(self, game, name, image, resource_mgr):
        self.debug_mode = False

        self.game = game
        self.name = name
        self.image = image
        self.resource_mgr = resource_mgr
        self.location = Vector2(0, 0)  # location always in "Viewport" coordinates
        self.destination = Vector2(0, 0)  # destination always in "Viewport" coordinates
        self.size = 1  # meters wide and tall
        self.speed = 0.  # meters/second

        self.brain = StateMachine()

        self.id = None  # Will be set by the Game

        self.prev_destination = None
        self.redirect_timer = None

    def __str__(self):
        return self.name + ':' + str(self.id) + ' - ' + self.brain.active_state.name

    def draw(self, surface):
        # Convert the "Viewport" coordinates into "Device" coordinates for drawing
        dev_location = self.game.scene.get_dev_vec_from_vp_vec(self.location)

        width, height = self.image.get_size()
        surface.blit(self.image, (dev_location.x - width / 2, dev_location.y - height / 2))

        if self.debug_mode:
            if self.brain is not None and self.brain.active_state is not None:
                debug_letter = self.brain.active_state.name[:2]
                if len(debug_letter) == 2:
                    surface.blit(self.resource_mgr.font.render(debug_letter, True, (0, 0, 0)), dev_location)

    def tick(self, time_passed):
        """ Triggers the entities StateMachine and locomotion """
        self.brain.think()

        if self.speed > 0 and self.location != self.destination:
            self._check_collisions_(time_passed)
            self._move_(time_passed)

    def get_random_destination(self):
        """ Returns a random vector within the viewport """
        return Vector2(randint(0, self.game.scene.viewport_rect.right), randint(0, self.game.scene.viewport_rect.bottom))

    def _check_collisions_(self, time_passed):
        """ Checks to see if the entities current location is too close
            to another entity, if so then the entity will attempt to spread out a bit."""
        if self.redirect_timer is None:
            # Check to make sure the entity isn't too close to another.
            collision_distance = 10
            blocking_entity = self.game.get_close_entity(None, self.location, collision_distance, self.id)

            if blocking_entity is not None:
                if self.debug_mode:
                    print(f"{self.name}-{self.id}: Too close to {blocking_entity.name}-{blocking_entity.id}, avoiding!")
                
                self.prev_destination = self.destination
                self.destination = self.get_random_destination()
                self.redirect_timer = .2  # 200 ms
        else:
            if self.redirect_timer > 0:
                # Currently redirecting, decrement timer by time passed
                if self.debug_mode:
                    print(f"{self.name}-{self.id}: Still avoiding for {self.redirect_timer}!")

                self.redirect_timer -= time_passed
            else:
                # redirecting time expired, reset destination
                if self.debug_mode:
                    print(f"{self.name}-{self.id}: Completed avoidance.")
                    
                self.destination = self.prev_destination
                self.prev_destination = None
                self.redirect_timer = None

    def _move_(self, time_passed):
        """ Provides locomotion for the entity while ensuring it stays within the viewport. """
        vec_to_destination = self.destination - self.location
        distance_to_destination = vec_to_destination.length()
        heading = vec_to_destination.normalize()
        travel_distance = min(distance_to_destination, time_passed * self.speed)
        self.location = self.location + travel_distance * heading

        # Ensure the entity stays within the boundaries:
        if self.location.x < 0:
            self.location.x = 0
        if self.location.x > self.game.scene.viewport_rect.right:
            self.location.x = self.game.scene.viewport_rect.right
        if self.location.y < 0:
            self.location.y = 0
        if self.location.y > self.game.scene.viewport_rect.bottom:
            self.location.y = self.game.scene.viewport_rect.bottom


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
