import pygame
import math
import os
from .environment import Environment

'''
This class defines the tank's shells.
A shell inherits from the environment class since we will use it as an inanimate object on our board.
Each shell checks for collisions with the wood boxes in order to decide whether they keep going.
'''

class Shell(Environment):
    def __init__(self, raw_image, position, speed, dir):
        super(Shell, self).__init__(raw_image, position)
        # Set the shell direction to the direction it was shot from
        self.__direction = dir

        self.IMAGES = {
            "shell_right1": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_right1.png')), (8, 8)).convert_alpha(),
            "shell_right2": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_right2.png')), (8, 8)).convert_alpha(),
            "shell_up1": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_up1.png')), (8, 8)).convert_alpha(),
            "shell_up2": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_up2.png')), (8, 8)).convert_alpha(),
            "shell_left1": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_left1.png')), (8, 8)).convert_alpha(),
            "shell_left2": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_left2.png')), (8, 8)).convert_alpha(),
            "shell_down1": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/shell_down1.png')), (8, 8)).convert_alpha(),
            "shell_down2": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/down2.png')), (20, 20)).convert_alpha(),
            "boom3": pygame.transform.scale(pygame.image.load(os.path.join(dir, 'assets/boom3.png')), (16, 16)).convert_alpha()
        }
        # The speed of a shell is set
        self.__speed = speed

    # Update the image of a shell
    def updateImage(self, raw_image):
        self.image = raw_image

    # Getters and Setters for private variables
    def getSpeed(self):
        return self.__speed

    def setSpeed(self, speed):
        self.__speed = speed

    def getDirection(self):
        return self.__direction

    # Move the shell in the required direction
    def continuousUpdate(self, wallGroup):
        # We are moving UP, so update the shell's image upwards
        if self.__direction == 0:
            self.update(self.IMAGES["shell_up1"], self.__speed)
            # When we hit a wall, we explode
            if self.checkCollision(wallGroup):
                self.update(self.IMAGES["shell_up2"], 0)
        # We are moving RIGHT, so update the shell's image to the right        
        if self.__direction == 1:
            self.update(self.IMAGES["shell_right1"], self.__speed)
            # When we hit a wall, we explode
            if self.checkCollision(wallGroup):
                self.update(self.IMAGES["shell_right2"], 0)
        # We are moving DOWN, so update the shell's image downards        
        if self.__direction == 2:
            self.update(self.IMAGES["shell_down1"], self.__speed)
            # When we hit a wall, we explode
            if self.checkCollision(wallGroup):
                self.update(self.IMAGES["shell_down2"], 0)
        # We are moving LEFT, so update the shell's image to the left
        if self.__direction == 3:
            self.update(self.IMAGES["shell_left1"], self.__speed)
            # When we hit a wall, we explode
            if self.checkCollision(wallGroup):
                self.update(self.IMAGES["shell_left2"], 0)

    # Move the shell in the required direction with the required speed (value), then set its image
    def update(self, raw_image, value):
        if self.__direction == 0: # UP
            self.setPosition(
                (self.getPosition()[0],
                 self.getPosition()[1] - value))
            self.image = raw_image
        if self.__direction == 1: # RIGHT
            self.setPosition(
                (self.getPosition()[0] + value,
                 self.getPosition()[1]))
            self.image = raw_image
        if self.__direction == 2: # DOWN
            self.setPosition(
                (self.getPosition()[0],
                 self.getPosition()[1] + value))
            self.image = raw_image
        if self.__direction == 3: # LEFT
            self.setPosition(
                (self.getPosition()[0] - value,
                 self.getPosition()[1]))
            self.image = raw_image
        self.rect.center = self.getPosition()

    '''
    We check for collisions in the direction the shell is moving by moving forward a little,
    checking for collisions, then moving back to the shell's original location.
    '''
    def checkCollision(self, colliderGroup):        
        if self.__direction == 0:
            self.update(self.image, self.__speed) # check UP collision
        if self.__direction == 1:
            self.update(self.image, self.__speed) # check RIGHT collision
        if self.__direction == 2:
            self.update(self.image, self.__speed) # check DOWN collision
        if self.__direction == 3:
            self.update(self.image, self.__speed) # check LEFT collision    
        Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
        if self.__direction == 0:
            self.update(self.image, -self.__speed) # reverese the UP movement
        if self.__direction == 1:
            self.update(self.image, -self.__speed) # reverse the RIGHT movement
        if self.__direction == 2:
            self.update(self.image, -self.__speed) # reverse the DOWN movement
        if self.__direction == 3:
            self.update(self.image, -self.__speed) # reverese the LEFT movement 
        return Colliders