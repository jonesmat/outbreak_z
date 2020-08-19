import pygame
from pygame import Rect
from pygame.math import Vector2


class Scene():
    
    def __init__(self):
        self.world_rect = Rect(0, 0, 1, 1)
        self.device_rect = Rect(0, 0, 1, 1)

    def get_world_x_from_dev_x(self, dev_x: float) -> float:
        ratio = self.device_rect.w / self.world_rect.w
        device_shift = dev_x - self.device_rect.x
        world_shift = device_shift / ratio

        return self.world_rect.x + world_shift

    def get_world_y_from_dev_y(self, dev_y: float) -> float:
        ratio = self.device_rect.h / self.world_rect.h
        device_shift = dev_y - self.device_rect.y
        world_shift = device_shift / ratio

        return self.world_rect.y + world_shift

    def get_dev_x_from_world_x(self, world_x: float) -> float:
        ratio = self.world_rect.w / self.device_rect.w
        world_shift = world_x - self.world_rect.x
        dev_shift = world_shift / ratio

        return self.device_rect.x + dev_shift

    def get_dev_y_from_world_y(self, world_y: float) -> float:
        ratio = self.world_rect.h / self.device_rect.h
        world_shift = world_y - self.world_rect.y
        dev_shift = world_shift / ratio

        return self.device_rect.y + dev_shift

    def get_dev_vec_from_world_points(self, world_x: float, world_y: float) -> Vector2:
        dev_x = self.get_dev_x_from_world_x(world_x)
        dev_y = self.get_dev_y_from_world_y(world_y)

        return Vector2(dev_x, dev_y)

    def get_world_vec_from_device_points(self, dev_x: float, dev_y: float) -> Vector2:
        world_x = self.get_world_x_from_dev_x(dev_x)
        world_y = self.get_world_y_from_dev_y(dev_y)

        return Vector2(world_x, world_y)

    def get_dev_vec_from_world_vec(self, world_vec: Vector2) -> Vector2:
        return self.get_dev_vec_from_world_points(world_vec.x, world_vec.y)

    def get_world_vec_from_device_vec(self, dev_vec: Vector2) -> Vector2:
        return self.get_world_vec_from_device_points(dev_vec.x, dev_vec.y)

