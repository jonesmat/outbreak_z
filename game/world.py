""" This module contains the World class """

from pygame.math import Vector2

from entities.survivor.entity import Survivor, Supplies


class World(object):
    """ The World class keeps track of all entities within its bounds. """

    def __init__(self, resource_mgr, screen_bounds):
        self.resource_mgr = resource_mgr
        self.background = resource_mgr.background_image
        self.bounds = screen_bounds

        self.entities = {}  # Store all the entities
        self.entity_id = 0  # Last entity id assigned

        self.supply = 0.0

    def add_entity(self, entity):
        """ Stores the entity then advances the current id """
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        """ Removes the entity from the world """
        del self.entities[entity.id]

    def get(self, entity_id):
        """ Find the entity, given its id """
        if entity_id in self.entities:
            return self.entities[entity_id]
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
        surface.blit(self.background, (0, 0))

        for entity in self.entities.values():
            entity.draw(surface)

    def get_close_entity(self, name, location, radius=100., ignore_id=None):
        """ Finds the first entity within range of a location """
        location = Vector2(location)

        for entity in self.entities.values():
            # If an ignore_id is passed, ignore the entity with that id.
            if ignore_id is not None and entity.id == ignore_id:
                continue

            if name is None or entity.name == name:
                distance = location.distance_to(entity.location)
                if distance < radius:
                    return entity
        return None

    def get_closest_entity(self, name, location, radius=100.):
        """ Find the closest entity within range of a location """
        location = Vector2(location)

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

    def get_close_entity_in_state(self, name, states, location, radius=100.):
        """ Find an entity within range of a location that is in one of the
            states provided. """
        location = Vector2(location)
        for entity in self.entities.values():
            if entity.name == name:
                for state in states:
                    if entity.brain.active_state.name == state:
                        distance = location.distance_to(entity.location)
                        if distance < radius:
                            return entity
        return None

    def get_entity_count(self, name):
        """ Gets the number of entities in the world with that name. """
        count = 0
        for entity in self.entities.values():
            if entity.name == name:
                count += 1
        return count

    def spawn_entity(self, entity_type, x_point, y_point):
        if self.supply - entity_type.supply_cost >= 0:
            if entity_type is Survivor:
                survivor = Survivor(self, self.resource_mgr)
                survivor.location = Vector2(x_point, y_point)
                survivor.brain.set_state("exploring")
                self.add_entity(survivor)
                self.supply -= 3
            elif entity_type is Supplies:
                supplies = Supplies(self, self.resource_mgr)
                supplies.location = Vector2(x_point, y_point)
                self.add_entity(supplies)
                self.supply -= 1

    def set_debug_mode(self, debug_mode):
        for entity in self.entities.values():
            entity.debug_mode = debug_mode