from random import randint

import pygame

from entities.game_base import State


class BloodStateFading(State):
    """ BloodSplat's natural state, fading away... """

    def __init__(self, blood):
        # Call the base class constructor to init the State
        State.__init__(self, "fading")
        # Set the survivor that this State will manipulate
        self.blood = blood

    def do_actions(self):
        alpha = self.blood.image.get_alpha()
        self.blood.image.set_alpha(alpha - 1)

    def check_conditions(self):
        alpha = self.blood.image.get_alpha()
        if alpha <= 0:
            self.blood.game.remove_entity(self.blood)

    def entry_actions(self):
        self.blood.image.set_alpha(255)
