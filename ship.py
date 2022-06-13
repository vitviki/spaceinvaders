# Abstract Ship class. 
# Every other ship in the game will be an object of this ship
import constants
import projectile
import pygame

class Ship:

    def __init__(self, x, y, health = 100):

        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.projectile_img = None
        self.projectiles = []
        self.cool_down_counter = 0

    def draw(self, window):
        
        pygame.draw.rect(window, constants.RED, (self.x, self.y, 50, 50))
        # window.blit(self.ship_img, (self.x, self.y))
        # for projectile in self.projectiles:
        #     projectile.draw(window)

    def move_projectiles(self, velocity, obj):

        self.cooldown()
        for projectile in self.projectiles:

            projectile.move(velocity)
            if projectile.off_screen(constants.WINDOW_SIZE[1]):
                self.projectiles.remove(projectile)
            elif projectile.collision(obj):
                obj.health -= 10
                self.projectiles.remove(projectile)

    def cooldown(self):

        if self.cool_down_counter >= constants.SHIP_COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):

        if self.cool_down_counter == 0:
            projectile = projectile.Projectile(self.x, self.y, self.projectile_img)
            self.projectiles.append(projectile)
            self.cool_down_counter = 1

    def get_width(self):

        return self.ship_img.get_width()

    def get_height(self):

        return self.ship_img.get_height()

