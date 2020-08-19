""" This module contains the Game class """

from pygame.math import Vector2

from entities.survivor.entity import Survivor
from entities.supplycrate.entity import SupplyCrate
from entities.zombie.entity import Zombie


class Game(object):

    def __init__(self, resource_mgr, scene):
        self.resource_mgr = resource_mgr
        self.background = resource_mgr.background_image
        self.scene = scene

        self.entities = {}  # Store all the entities
        self.next_entity_id = 0  # Next entity id assigned

        self.supply = 0.0

    def add_entity(self, entity):
        """ Stores the entity then advances the current id """
        self.entities[self.next_entity_id] = entity
        entity.id = self.next_entity_id
        self.next_entity_id += 1

    def remove_entity(self, entity):
        """ Removes the entity from the game """
        del self.entities[entity.id]

    def get(self, id):
        """ Find the entity, given its id """
        if id in self.entities:
            return self.entities[id]
        else:
            return None

    def tick(self, time_passed):
        """ Call the tick method of each GameEntity """
        time_passed_seconds = time_passed / 1000.0

        self.supply += time_passed_seconds / 2

        local_entities = list(self.entities.values())
        for entity in local_entities:
            try:
                entity.tick(time_passed_seconds)
            except KeyError:
                pass

    def draw(self, surface):
        self._draw_background(surface)

        for entity in self.entities.values():
            entity.draw(surface)

    def _draw_background(self, surface):
        background_width, background_height = self.background.get_size()

        drawn_x = 0
        while drawn_x < self.scene.device_rect.right:
            
            drawn_y = 0
            while drawn_y < self.scene.device_rect.bottom:
                surface.blit(self.background, (drawn_x, drawn_y))
                drawn_y += background_height

            drawn_x += background_width
        

    def get_close_entity(self, name, location: Vector2, radius=20., ignore_id=None):
        """ Finds the first entity within range of a location """

        for entity in self.entities.values():
            # If an ignore_id is passed, ignore the entity with that id.
            if ignore_id is not None and entity.id == ignore_id:
                continue

            if name is None or entity.name == name:
                distance = location.distance_to(entity.location)
                if distance < radius:
                    return entity
        return None

    def get_closest_entity(self, name, location: Vector2, radius=20.):
        """ Find the closest entity within range of a location """

        close_entities = []
        for entity in self.entities.values():
            if name is None or entity.name == name:
                distance = location.distance_to(entity.location)
                if distance < radius:
                    close_entities.append((distance, entity))

        # Return the closest of the entities within range.
        if len(close_entities) > 0:
            close_entities = sorted(close_entities, key=lambda e: e[0])
            distance, closest_entity = close_entities[0]
            return closest_entity

        return None

    def get_close_entity_in_state(self, name, states, location: Vector2, radius=20.):
        """ Find an entity within range of a location that is in one of the
            states provided. """

        for entity in self.entities.values():
            if entity.name == name:
                for state in states:
                    if entity.brain.active_state.name == state:
                        distance = location.distance_to(entity.location)
                        if distance < radius:
                            return entity
        return None

    def get_entity_count(self, name):
        """ Gets the number of entities in the game with that name. """
        count = 0
        for entity in self.entities.values():
            if entity.name == name:
                count += 1
        return count

    def spawn_entity_at_device(self, entity_type, x_point, y_point):
        if self.supply - entity_type.SUPPLY_COST >= 0:
            if entity_type is Survivor:
                survivor = Survivor(self, self.resource_mgr)
                survivor.location = self.scene.get_vp_vec_from_device_points(x_point, y_point)
                survivor.brain.set_state("exploring")
                self.add_entity(survivor)
                self.supply -= 3
            elif entity_type is SupplyCrate:
                supplycrate = SupplyCrate(self, self.resource_mgr)
                supplycrate.location = self.scene.get_vp_vec_from_device_points(x_point, y_point)
                self.add_entity(supplycrate)
                self.supply -= 1

    def set_debug_mode(self, debug_mode):
        for entity in self.entities.values():
            entity.debug_mode = debug_mode

    def turn_survivor(self, survivor):
        ''' Turns a survivor into a Zombie! '''
            
        self.remove_entity(survivor)

        new_zombie = Zombie(self, self.resource_mgr)
        new_zombie.location = Vector2(survivor.location.x, survivor.location.y)
        new_zombie.brain.set_state("wandering")
        self.add_entity(new_zombie)