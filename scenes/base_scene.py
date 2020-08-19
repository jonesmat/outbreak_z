import pygame
from pygame import Rect
from pygame.math import Vector2


class Scene():
    
    def __init__(self):
        self.viewport_rect = Rect(0, 0, 1, 1)
        self.device_rect = Rect(0, 0, 1, 1)

    def get_vp_x_from_dev_x(self, dev_x: float) -> float:
        ratio = self.device_rect.w / self.viewport_rect.w
        device_shift = dev_x - self.device_rect.x
        vp_shift = device_shift / ratio

        return self.viewport_rect.x + vp_shift

    def get_vp_y_from_dev_y(self, dev_y: float) -> float:
        ratio = self.device_rect.h / self.viewport_rect.h
        device_shift = dev_y - self.device_rect.y
        vp_shift = device_shift / ratio

        return self.viewport_rect.y + vp_shift

    def get_dev_x_from_vp_x(self, vp_x: float) -> float:
        ratio = self.viewport_rect.w / self.device_rect.w
        vp_shift = vp_x - self.viewport_rect.x
        dev_shift = vp_shift / ratio

        return self.device_rect.x + dev_shift

    def get_dev_y_from_vp_y(self, vp_y: float) -> float:
        ratio = self.viewport_rect.h / self.device_rect.h
        vp_shift = vp_y - self.viewport_rect.y
        dev_shift = vp_shift / ratio

        return self.device_rect.y + dev_shift

    def get_dev_vec_from_vp_points(self, vp_x: float, vp_y: float) -> Vector2:
        dev_x = self.get_dev_x_from_vp_x(vp_x)
        dev_y = self.get_dev_y_from_vp_y(vp_y)

        return Vector2(dev_x, dev_y)

    def get_vp_vec_from_device_points(self, dev_x: float, dev_y: float) -> Vector2:
        vp_x = self.get_vp_x_from_dev_x(dev_x)
        vp_y = self.get_vp_y_from_dev_y(dev_y)

        return Vector2(vp_x, vp_y)

    def get_dev_vec_from_vp_vec(self, vp_vec: Vector2) -> Vector2:
        return self.get_dev_vec_from_vp_points(vp_vec.x, vp_vec.y)

    def get_vp_vec_from_device_vec(self, dev_vec: Vector2) -> Vector2:
        return self.get_vp_vec_from_device_points(dev_vec.x, dev_vec.y)

