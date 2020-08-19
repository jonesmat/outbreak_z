import pygame
from pygame import Rect


class Scene():
    
    def __init__(self):
        self.viewport_rect = Rect(0, 0, 1, 1)
        self.device_rect = Rect(0, 0, 1, 1)

    def get_vp_x_from_dev_x(self, dev_x):
        ratio = self.device_rect.w / self.viewport_rect.w
        device_shift = dev_x - self.device_rect.x
        vp_shift = device_shift / ratio

        return self.viewport_rect.x + vp_shift

    def get_vp_y_from_dev_y(self, dev_y):
        ratio = self.device_rect.h / self.viewport_rect.h
        device_shift = dev_y - self.device_rect.y
        vp_shift = device_shift / ratio

        return self.viewport_rect.y + vp_shift

    def get_dev_x_from_vp_x(self, vp_x):
        ratio = self.device_rect.w / self.viewport_rect.w
        vp_shift = vp_x - self.viewport_rect.x
        dev_shift = vp_shift / ratio

        return self.device_rect.x + dev_shift

    def get_dev_y_from_vp_y(self, vp_y):
        ratio = self.device_rect.h / self.viewport_rect.h
        vp_shift = vp_y - self.viewport_rect.y
        dev_shift = vp_shift / ratio

        return self.device_rect.y + dev_shift
