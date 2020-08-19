from entities.game_base import State
from entities.bloodsplat.entity import BloodSplat


class BulletStateSeeking(State):
    """ Controls the seeking of the Bullet towards its target """

    def __init__(self, bullet, resource_mgr):
        # Call the base class constructor to init the State
        State.__init__(self, "seeking")
        # Set the survivor that this State will manipulate
        self.bullet = bullet
        self.resource_mgr = resource_mgr
        self.zombie_id = None

    def do_actions(self):
        # If the bullet has hit the zombie...
        zombie = self.bullet.game.get(self.bullet.zombie_id)
        if zombie is not None:
            if self.bullet.location.distance_to(zombie.location) <= 0.2:
                zombie.health -= 1
                if zombie.health <= 0:
                    self.bullet.game.remove_entity(zombie)

                    blood = BloodSplat(self.bullet.game, self.resource_mgr)
                    blood.brain.set_state("fading")
                    blood.location = zombie.location
                    self.bullet.game.add_entity(blood)

                self.bullet.game.remove_entity(self.bullet)
            else:
                # Reset the destination to the new zombie path.
                self.bullet.destination = zombie.location

    def check_conditions(self):
        zombie = self.bullet.game.get(self.bullet.zombie_id)
        if zombie is None:
            self.bullet.game.remove_entity(self.bullet)

    def entry_actions(self):
        # Target the zombie.
        self.bullet.speed = self.bullet.BASE_SPEED
        zombie = self.bullet.game.get(self.bullet.zombie_id)
        if zombie is not None:
            self.bullet.destination = zombie.location


