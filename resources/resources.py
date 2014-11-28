""" Sets up all resources used by outbreak_z """

import pygame


class Resources(object):
    """ Contains all external resources used by the game. """

    def __init__(self):
        self.font = None

        self.background_image = pygame.image.load('resources/background.jpg').convert()
        self.zombie_image = pygame.image.load('resources/zombie.png').convert_alpha()
        self.survivor_image = pygame.image.load('resources/survivor.png').convert_alpha()
        self.survivor_dead_image = pygame.image.load('resources/survivor_dead.png').convert_alpha()
        self.survivor_hit_image = pygame.image.load('resources/survivor_hit.png').convert_alpha()
        self.supplies_image = pygame.image.load('resources/supplies.png').convert_alpha()
        self.bullet_image = pygame.image.load('resources/bullet.png').convert_alpha()
        self.blood_splat_image = pygame.image.load('resources/blood_splat.png').convert_alpha()
        self.graveyard_image = pygame.image.load('resources/graveyard.png').convert_alpha()
        self.caution_image = pygame.image.load('resources/caution.png').convert_alpha()