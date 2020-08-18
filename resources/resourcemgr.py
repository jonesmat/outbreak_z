""" Sets up all resources used by outbreak_z """

import pygame


class ResourceMgr(object):
    """ Contains all external resources used by the game. """

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 16)

        self.background_image = pygame.image.load('resources/background.jpg').convert()
        self.zombie_image = pygame.image.load('resources/zombie.png').convert_alpha()
        self.bullet_image = pygame.image.load('resources/bullet.png').convert_alpha()
        self.blood_splat_image = pygame.image.load('resources/blood_splat.png').convert_alpha()
        self.caution_image = pygame.image.load('resources/caution.png').convert_alpha()