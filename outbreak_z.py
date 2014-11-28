"""
    Requires:
        python 2.7.3
        pygame-1.9.2a0
        
        
    TODO:
        - Give a random chance of a survivor finding a shotgun in a crate.
        - Allow Survivors to destroy a graveyard.
"""

from sys import exit
import pygame
from pygame.locals import HWSURFACE, FULLSCREEN, QUIT, KEYDOWN, K_q, \
    K_ESCAPE, K_BACKQUOTE, MOUSEBUTTONDOWN
from pygame.math import Vector2
import pygame._view # Fixes a py2exe packaging issue
from random import randint
from resources import Resources
from world import World
from ui import UI
from zombie import Zombie
from survivor import Survivor, Supplies
from graveyard import Graveyard


pygame.init()

SCREEN_SIZE = (800, 600)
#screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | FULLSCREEN, 32)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

resources = Resources(pygame)

font = pygame.font.SysFont("arial", 16)
debug_mode = False

world = World(resources, SCREEN_SIZE)
world.supply = 20
ui = UI()
clock = pygame.time.Clock()
w, h = SCREEN_SIZE

# Spawn a few graveyards
for _ in range(1, randint(3, 6)):
    spawn_loc = Vector2(randint(0, w), randint(0, h))
    graveyard = Graveyard(world, resources.graveyard_image, resources.zombie_image)
    graveyard.location = Vector2(spawn_loc.x, spawn_loc.y)
    graveyard.brain.set_state("spawning")
    world.add_entity(graveyard)


while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE:
                exit()
            if event.key == K_BACKQUOTE:
                debug_mode = not debug_mode
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x_point, y_point = pygame.mouse.get_pos()
                world.spawn_entity(Survivor, x_point, y_point)
            if event.button == 3:
                x_point, y_point = pygame.mouse.get_pos()
                world.spawn_entity(Supplies, x_point, y_point)
    
    time_passed = clock.tick(30)
    
    world.process(time_passed)
    world.render(screen, font, debug_mode)
    ui.render(screen, font, world)
    
    if debug_mode:
        debug_text = 'Debug: '
        screen.blit(font.render(debug_text, True, (0, 0, 0)), (0, 0))
    
    pygame.display.update()

