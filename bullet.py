"""
    Bullet is fired from the Survivor when attacking.
"""

from random import randint
import pygame
from game_base import GameEntity, State


class Bullet(GameEntity):
    """ Bullet is fired from the Survivor when attacking. """
    def __init__(self, world, image, blood_image):
        GameEntity.__init__(self, world, "bullet", image)
        
        # Create an instance of each of the states
        seeking_state = BulletStateSeeking(self)
        # Add the states to the state machine
        self.brain.add_state(seeking_state)
        
        self.blood_image = blood_image
        self.zombie_id = None
    
    
class BulletStateSeeking(State):
    """ Controls the seeking of the Bullet towards its target """
    def __init__(self, bullet):
        # Call the base class constructor to init the State
        State.__init__(self, "seeking")
        # Set the survivor that this State will manipulate
        self.bullet = bullet
        self.zombie_id = None
    
    def do_actions(self):
        # If the bullet has hit the zombie...
        zombie = self.bullet.world.get(self.bullet.zombie_id)
        if zombie is not None:
            if self.bullet.location.distance_to(zombie.location) <= 2.0:
                zombie.health -= 1
                if zombie.health <= 0:
                    self.bullet.world.remove_entity(zombie)
                    
                    blood = BloodSplat(self.bullet.world, 
                        self.bullet.blood_image)
                    blood.brain.set_state("fading")
                    blood.location = zombie.location
                    self.bullet.world.add_entity(blood)
            
                self.bullet.world.remove_entity(self.bullet)
            else:
                # Reset the destination to the new zombie path.
                self.bullet.destination = zombie.location
    
    def check_conditions(self):
        zombie = self.bullet.world.get(self.bullet.zombie_id)
        if zombie is None:
            self.bullet.world.remove_entity(self.bullet)
    
    def entry_actions(self):
        # Target the zombie.
        self.bullet.speed = 200
        zombie = self.bullet.world.get(self.bullet.zombie_id)
        if zombie is not None:
            self.bullet.destination = zombie.location


class BloodSplat(GameEntity):
    """ When Bullet meets Zombie, splat! """
    def __init__(self, world, image):
        # Set random image rotation.
        rotate = pygame.transform.rotate
        rotation = randint(1, 360)
        GameEntity.__init__(self, world, "bloodsplat", rotate(image, rotation), 
            draw_priority=5)
        
        # Create an instance of each of the states
        fading_state = BloodStateFading(self)
        # Add the states to the state machine
        self.brain.add_state(fading_state)

        
class BloodStateFading(State):
    """ BloodSplat's natural state, fading away... """
    def __init__(self, blood):
        # Call the base class constructor to init the State
        State.__init__(self, "fading")
        # Set the survivor that this State will manipulate
        self.blood = blood
        
    def do_actions(self):
        alpha = self.blood.image.get_alpha()
        self.blood.image.set_alpha(alpha - 1)
        
    def check_conditions(self):
        alpha = self.blood.image.get_alpha()
        if alpha <= 0:
            self.blood.world.remove_entity(self.blood)
            
    def entry_actions(self):
        self.blood.image.set_alpha(255)
