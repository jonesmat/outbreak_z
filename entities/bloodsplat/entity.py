from random import randint

import pygame

from entities.game_base import GameEntity
import entities.bloodsplat.states as states


class BloodSplat(GameEntity):
    """ When Bullet meets Zombie, splat! """

    def __init__(self, world, resource_mgr):
        self.blood_splat_image = pygame.image.load('entities/bloodsplat/blood_splat.png').convert_alpha()

        # Set random image rotation.
        rotate = pygame.transform.rotate
        rotation = randint(1, 360)
        GameEntity.__init__(self, world, "bloodsplat", rotate(self.blood_splat_image, rotation), resource_mgr)

        # Create an instance of each of the states
        fading_state = states.BloodStateFading(self)
        # Add the states to the state machine
        self.brain.add_state(fading_state)