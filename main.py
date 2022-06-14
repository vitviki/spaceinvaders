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
    ships['red_ship']           = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png')), constants.SHIP_SIZE_STANDARD)
    ships['green_ship']         = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png')), constants.SHIP_SIZE_STANDARD)
    ships['blue_ship']          = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png')), constants.SHIP_SIZE_STANDARD)
    ships['yellow_player_ship'] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png')), constants.SHIP_SIZE_STANDARD)
    
    # Projectiles
    projectiles['red']          = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
    projectiles['green']        = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
    projectiles['blue']         = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
    projectiles['yellow']       = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
    
    # Background
    backgrounds['black']        = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), constants.WINDOW_SIZE)

    # Font
    fonts['comicsans']          = pygame.font.SysFont('comicsans', 30)

class Player(ship.Ship):

    def __init__(self, x, y, ship_img, projectile_img, health=100):

        super().__init__(x, y, health)
        self.ship_img = ship_img
        self.projectile_img = projectile_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_projectiles(self, velocity, objs):

        self.cooldown()
        for projectile in self.projectiles:

            projectile.move(velocity)
            if projectile.off_screen(constants.WINDOW_SIZE[1]):
                self.projectiles.remove(projectile)
            else:
                for obj in objs:
                    if projectile.collision(obj):
                        objs.remove(obj)
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)

    def draw(self, window):

        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):

        pygame.draw.rect(window, constants.RED, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, constants.GREEN, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))

    
def main():

    run = True
    clock = pygame.time.Clock()
    current_level = constants.LEVEL
    current_lives = constants.LIVES
    player_velocity = constants.PLAYER_VELOCITY
    projectile_velocity = constants.PLAYER_PROJECTILE_VELOCITY
    ships = {}
    projectiles = {}
    backgrounds = {}
    fonts = {}

    loadAssets(ships, projectiles, backgrounds, fonts)

    player = Player(constants.PLAYER_SHIP_SPAWN_COORD[0], constants.PLAYER_SHIP_SPAWN_COORD[1], ships['yellow_player_ship'], projectiles['yellow'])

    def redraw_window():
        
        # Render background image
        WINDOW.blit(backgrounds['black'], (0, 0))

        # Draw in game text
        lives_label = fonts['comicsans'].render(f"Lives: {current_lives}",1, constants.WHITE)
        level_label = fonts['comicsans'].render(f"Level: {current_level}",1, constants.WHITE)

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (constants.WINDOW_SIZE[0] - lives_label.get_width() - 10, 10 ))

        player.draw(WINDOW)
        pygame.display.update()



    while run:

        clock.tick(constants.FPS)
        redraw_window()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player.ship_img.get_width() < constants.WINDOW_SIZE[0]:
            player.x += player_velocity 
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player.ship_img.get_height() < constants.WINDOW_SIZE[1]:
            player.y += player_velocity

        if keys[pygame.K_SPACE]:
            player.shoot()

        player.move_projectiles(-projectile_velocity, [])
        
        

main()