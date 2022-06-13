import pygame
import os
import time
import random
import constants
import ship
import projectile

pygame.font.init()
WINDOW                      = pygame.display.set_mode(constants.WINDOW_SIZE)
pygame.display.set_caption("Space Invaders")

# Load assets
def loadAssets(ships, projectiles, backgrounds, fonts):
    
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
    backgrounds['black']        = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), constants.WINDOW_SIZE)

    # Font
    fonts['comicsans']          = pygame.font.SysFont('comicsans', 30)

def main():

    run = True
    clock = pygame.time.Clock()
    current_level = constants.LEVEL
    current_lives = constants.LIVES
    ships = {}
    projectiles = {}
    backgrounds = {}
    fonts = {}

    loadAssets(ships, projectiles, backgrounds, fonts)

    sample = ship.Ship(200, 400)

    def redraw_window():
        
        # Render background image
        WINDOW.blit(backgrounds['black'], (0, 0))

        # Draw in game text
        lives_label = fonts['comicsans'].render(f"Lives: {current_lives}",1, constants.WHITE)
        level_label = fonts['comicsans'].render(f"Level: {current_level}",1, constants.WHITE)

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (constants.WINDOW_SIZE[0] - lives_label.get_width() - 10, 10 ))

        sample.draw(WINDOW)

        pygame.display.update()



    while run:

        clock.tick(constants.FPS)
        redraw_window()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

main()