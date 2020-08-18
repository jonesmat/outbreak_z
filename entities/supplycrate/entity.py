import pygame

from entities.game_base import GameEntity


class SupplyCrate(GameEntity):
    supply_cost = 1

    """ Simple supply entity """
    def __init__(self, world, resource_mgr):
        
        self.supplycrate_image = pygame.image.load('entities/supplycrate/supplycrate.png').convert_alpha()

        GameEntity.__init__(self, world, "supplycrate", self.supplycrate_image, resource_mgr)
