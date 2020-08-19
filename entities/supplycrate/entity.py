import pygame

from entities.base_entity import GameEntity


class SupplyCrate(GameEntity):
    SIZE = 1  # meters wide and tall
    SUPPLY_COST = 1

    """ Simple supply entity """
    def __init__(self, game, resource_mgr):
        
        self.supplycrate_image = pygame.image.load('entities/supplycrate/supplycrate.png').convert_alpha()

        GameEntity.__init__(self, game, "supplycrate", self.supplycrate_image, resource_mgr)

        self.size = SupplyCrate.SIZE
