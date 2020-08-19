import pygame
from pygame import Rect
from pygame.math import Vector2


class Scene():
    
    def __init__(self):
        self.viewport_rect = Rect(0, 0, 1, 1)
        self.device_rect = Rect(0, 0, 1, 1)

    def get_viewport_x_from_dev_x(self, dev_x: float) -> float:
        ratio = self.device_rect.w / self.viewport_rect.w
        device_shift = dev_x - self.device_rect.x
        viewport_shift = device_shift / ratio

        return self.viewport_rect.x + viewport_shift

    def get_viewport_y_from_dev_y(self, dev_y: float) -> float:
        ratio = self.device_rect.h / self.viewport_rect.h
        device_shift = dev_y - self.device_rect.y
        viewport_shift = device_shift / ratio

        return self.viewport_rect.y + viewport_shift

    def get_dev_x_from_viewport_x(self, viewport_x: float) -> float:
        ratio = self.viewport_rect.w / self.device_rect.w
        viewport_shift = viewport_x - self.viewport_rect.x
        dev_shift = viewport_shift / ratio

        return self.device_rect.x + dev_shift

    def get_dev_y_from_viewport_y(self, viewport_y: float) -> float:
        ratio = self.viewport_rect.h / self.device_rect.h
        viewport_shift = viewport_y - self.viewport_rect.y
        dev_shift = viewport_shift / ratio

        return self.device_rect.y + dev_shift

    def get_dev_vec_from_viewport_points(self, viewport_x: float, viewport_y: float) -> Vector2:
        dev_x = self.get_dev_x_from_viewport_x(viewport_x)
        dev_y = self.get_dev_y_from_viewport_y(viewport_y)

        return Vector2(dev_x, dev_y)

    def get_viewport_vec_from_device_points(self, dev_x: float, dev_y: float) -> Vector2:
        viewport_x = self.get_viewport_x_from_dev_x(dev_x)
        viewport_y = self.get_viewport_y_from_dev_y(dev_y)

        return Vector2(viewport_x, viewport_y)

    def get_dev_vec_from_viewport_vec(self, viewport_vec: Vector2) -> Vector2:
        return self.get_dev_vec_from_viewport_points(viewport_vec.x, viewport_vec.y)

    def get_viewport_vec_from_device_vec(self, dev_vec: Vector2) -> Vector2:
        return self.get_viewport_vec_from_device_points(dev_vec.x, dev_vec.y)

