import pygame
import os
import time
import random

################# GAME WINDOW CONSTANTS #################
WINDOW_SIZE                 = width, height = 750, 750
WINDOW                      = pygame.display.set_mode(WINDOW_SIZE)
FPS                         = 60
pygame.display.set_caption("Space Invaders")


# Load assets
def loadAssets(ships, projectiles, backgrounds):
    
    # Ships
    ships['red_ship']           = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
    ships['green_ship']         = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
    ships['blue_ship']          = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
    ships['yellow_player_ship'] = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))
    
    # Projectiles
    projectiles['red']          = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
    projectiles['green']        = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
    projectiles['blue']         = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
    projectiles['yellow']       = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
    
    # Background
    backgrounds['black']        = pygame.image.load(os.path.join('assets', 'background-black.png'))

def main():

    run = True
    clock = pygame.time.Clock()
    ships = {}
    projectiles = {}
    backgrounds = {}

    loadAssets(ships, projectiles, backgrounds)

    def redraw_window():
        
        pygame.display.update()


    while run:

        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

main()