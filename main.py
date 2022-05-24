import pygame
import os
import time
import random

pygame.font.init()

################# GAME WINDOW CONSTANTS #################
WINDOW_SIZE                 = width, height = 750, 750
WINDOW                      = pygame.display.set_mode(WINDOW_SIZE)
FPS                         = 60
pygame.display.set_caption("Space Invaders")

################ COLORS #################
WHITE   = (255, 255, 255)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
ORANGE  = (255, 69, 0)
BLACK   = (0, 0, 0)


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
    backgrounds['black']        = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), WINDOW_SIZE)

    # Font
    fonts['comicsans']          = pygame.font.SysFont('comicsans', 30)

def main():

    run = True
    clock = pygame.time.Clock()
    level = 1
    lives = 5
    ships = {}
    projectiles = {}
    backgrounds = {}
    fonts = {}

    loadAssets(ships, projectiles, backgrounds, fonts)

    def redraw_window():
        
        # Render background image
        WINDOW.blit(backgrounds['black'], (0, 0))

        # Draw in game text
        lives_label = fonts['comicsans'].render(f"Lives: {lives}",1, WHITE)
        level_label = fonts['comicsans'].render(f"Level: {level}",1, WHITE)

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WINDOW_SIZE[0] - lives_label.get_width() - 10, 10 ))



        pygame.display.update()


    while run:

        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

main()