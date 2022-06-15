import pygame
import os
import time
import random
import constants
import ship
import projectile

pygame.font.init()
pygame.mixer.init()
WINDOW                      = pygame.display.set_mode(constants.WINDOW_SIZE)
pygame.display.set_caption("Space Invaders")

# Load assets
def loadAssets(ships, projectiles, backgrounds, fonts, sounds):
    
    # Ships
    ships['red']           = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png')), 180), constants.SHIP_SIZE_STANDARD)
    ships['green']         = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png')),180), constants.SHIP_SIZE_STANDARD)
    ships['blue']          = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png')), 180), constants.SHIP_SIZE_STANDARD)
    ships['yellow_player_ship'] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png')), constants.SHIP_SIZE_STANDARD)
    
    # Projectiles
    projectiles['red']          = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
    projectiles['green']        = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
    projectiles['blue']         = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
    projectiles['yellow']       = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
    
    # Background
    backgrounds['black']        = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), constants.WINDOW_SIZE)

    # Font
    fonts['comicsans_30']       = pygame.font.SysFont('comicsans', 30)
    fonts['comicsans_40']       = pygame.font.SysFont('comicsans', 40)
    fonts['comicsans_50']       = pygame.font.SysFont('comicsans', 50)    
    fonts['comicsans_60']       = pygame.font.SysFont('comicsans', 60)
    fonts['comicsans_70']       = pygame.font.SysFont('comicsans', 70)

    # Sounds
    sounds['fire']              = pygame.mixer.Sound(os.path.join('assets', 'projectile_fire.wav'))
    sounds['hit']               = pygame.mixer.Sound(os.path.join('assets', 'hit.wav'))
    sounds['winning']           = pygame.mixer.Sound(os.path.join('assets', 'winning.wav'))
    pygame.mixer.music.load(os.path.join('assets', 'game_music.wav'))

    #sounds['music']             = pygame.mixer.Sound(os.path.join('assets', 'game_music.wav'))


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

class Enemy(ship.Ship):

    def __init__(self, x, y, img, projectile_img, health=100):
        
        super().__init__(x, y, health)
        self.ship_img = img
        self.projectile_img = projectile_img
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        
        self.y += velocity
    
    def shoot(self):
        
        super().shoot()

def check_collision(obj1, obj2):

    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():

    run = True
    game_started = False
    clock = pygame.time.Clock()
    current_level = constants.LEVEL
    current_lives = constants.LIVES
    player_velocity = constants.PLAYER_VELOCITY
    enemy_velocity = constants.ENEMY_VELOCITY
    player_projectile_velocity = constants.PLAYER_PROJECTILE_VELOCITY
    enemy_projectile_velocity = constants.ENEMY_PROJECTILE_VELOCITY
    enemy_wave_length = constants.ENEMY_WAVE_LENGTH
    lost = False
    lose_count = 0
    ships = {}
    projectiles = {}
    backgrounds = {}
    fonts = {}
    sounds = {}

    loadAssets(ships, projectiles, backgrounds, fonts, sounds)

    pygame.mixer.Sound.set_volume(sounds['fire'], 0.05)
    pygame.mixer.Sound.set_volume(sounds['hit'], 0.05)
    pygame.mixer.Sound.set_volume(sounds['winning'], 0.1)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    player = Player(constants.PLAYER_SHIP_SPAWN_COORD[0], constants.PLAYER_SHIP_SPAWN_COORD[1], ships['yellow_player_ship'], projectiles['yellow'])
    enemies = []


    def redraw_window():
        
        # Render background image
        WINDOW.blit(backgrounds['black'], (0, 0))

        if game_started:

            # Draw in game text
            lives_label = fonts['comicsans_30'].render(f"Lives: {current_lives}",1, constants.WHITE)
            level_label = fonts['comicsans_30'].render(f"Level: {current_level}",1, constants.WHITE)

            WINDOW.blit(lives_label, (10, 10))
            WINDOW.blit(level_label, (constants.WINDOW_SIZE[0] - lives_label.get_width() - 10, 10 ))

            # Draw all the enemies
            for enemy in enemies:
                enemy.draw(WINDOW)

            player.draw(WINDOW)

            # Lost label
            if lost:
                lost_label = fonts['comicsans_60'].render("You Lost!", 1, constants.WHITE)
                WINDOW.blit(lost_label, (constants.WINDOW_SIZE[0] // 2 - lost_label.get_width() // 2, 350))

        else:

            title_label = fonts['comicsans_50'].render("Press mouse button to begin...", 1, constants.WHITE)
            WINDOW.blit(title_label, (constants.WINDOW_SIZE[0] // 2 - title_label.get_width() // 2, 350))

        pygame.display.update()



    while run:

        clock.tick(constants.FPS)
        redraw_window()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                game_started = True

        if game_started:
            if current_lives <= 0 or player.health <= 0:
                lost = True
                lose_count += 1

            if lost:
                if lose_count > constants.FPS * 3:
                    run = False
                else:
                    continue

            
            # Spawn enemies
            if len(enemies) == 0:
                if current_level >= 1:
                    sounds['winning'].play()
                    
                current_level += 1
                enemy_wave_length += 5
                for i in range(enemy_wave_length):

                    # Enemy and it's projectile color
                    color = random.choice(["red", "green", "blue"])
                    enemy = Enemy(random.randrange(50, constants.WINDOW_SIZE[0]), random.randrange(-1500, -100), ships[color], projectiles[color])
                    enemies.append(enemy)

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
                sounds['fire'].play()
                player.shoot()

            # Enemy movement.
            for enemy in enemies[:]:

                enemy.move(enemy_velocity)
                enemy.move_projectiles(enemy_projectile_velocity, player)
                
                if random.randrange(0, 2*60) == 1:
                    enemy.shoot()

                if check_collision(enemy, player):
                    player.health -= 10
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > constants.WINDOW_SIZE[1]:
                    enemies.remove(enemy)

            player.move_projectiles(-player_projectile_velocity, enemies)
        
        
main()