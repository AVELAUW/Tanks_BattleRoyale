from .environment import Environment
import pygame

'''
This class defines the walls in the game.
If you want, you can add traps or powerups to walls such to damage or heal the player.
'''


class Wall(Environment):

    def __init__(self, raw_image, position):
        super(Wall, self).__init__(raw_image, position)

    # Update the image (scale)
    def updateImage(self, raw_image):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (32, 32))
