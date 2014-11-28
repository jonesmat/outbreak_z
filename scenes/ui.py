""" UI handles the drawing of the ui...duh """

from pygame.math import Vector2


class UI(object):
    """ Draws the UI """

    @staticmethod
    def render(surface, font, world):
        """ Draws the UI """
        w_bound, h_bound = world.bounds

        zombies = "Zombies: " + str(world.get_entity_count("zombie"))
        surface.blit(font.render(zombies, True, (0, 0, 0)), Vector2(5, h_bound - 20))

        survivors = "Survivors: " + str(world.get_entity_count("survivor"))
        surface.blit(font.render(survivors, True, (0, 0, 0)), Vector2(120, h_bound - 20))

        res_str = "Supply Remaining: " + str(int(world.supply))
        surface.blit(font.render(res_str, True, (0, 0, 0)), Vector2(w_bound - 330, h_bound - 20))
