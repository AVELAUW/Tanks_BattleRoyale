import pygame
import sys
from pygame.constants import K_a, K_d, K_w, K_s, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN, KEYDOWN, KEYUP, QUIT
from .board import Board
from ple.games.base.pygamewrapper import PyGameWrapper
import numpy as np
import os


class TanksBattleRoyale(PyGameWrapper):
    def __init__(self):
        """
        Input parameters here
        
        """
        self.height = 352
        self.width = 352
        self.value = 10 # Shell speed

        actions = {
            "p1_left": K_a,
            "p1_right": K_d,
            "p1_up": K_w,
            "p1_down": K_s,
            "p1_fire": K_SPACE,
            "p2_left": K_LEFT,
            "p2_right": K_RIGHT,
            "p2_up": K_UP,
            "p2_down": K_DOWN,
            "p2_fire": K_RETURN
        }

        PyGameWrapper.__init__(self, self.width, self.height, actions=actions)

        self.rewards = {
            "p1_hit": -1,
            "p1_lost": -10,
            "p2_hit": -1,
            "p2_lost": -10,
            "tick": 0
        }

        self.allowed_fps = 30
        self._dir = os.path.dirname(os.path.abspath(__file__))
        self.IMAGES = {
            "tank_down1": pygame.image.load(os.path.join(self._dir, 'assets/tank_down1.png')),
            "tank_down2": pygame.image.load(os.path.join(self._dir, 'assets/tank_down2.png')),
            "tank_left1": pygame.image.load(os.path.join(self._dir, 'assets/tank_left1.png')),
            "tank_left2": pygame.image.load(os.path.join(self._dir, 'assets/tank_left2.png')),
            "tank_right1": pygame.image.load(os.path.join(self._dir, 'assets/tank_right1.png')),
            "tank_right2": pygame.image.load(os.path.join(self._dir, 'assets/tank_right2.png')),
            "tank_up1": pygame.image.load(os.path.join(self._dir, 'assets/tank_up1.png')),
            "tank_up2": pygame.image.load(os.path.join(self._dir, 'assets/tank_up2.png'))
        }

    def init(self):
        # Create a new instance of the Board class
        self.newGame = Board(
            self.width,
            self.height,
            self.value,
            self._dir)

        # Assign groups from the Board instance that was created
        self.playerGroup = self.newGame.playerGroup
        self.wallGroup = self.newGame.wallGroup
        self.shellGroup = self.newGame.shellGroup
        self.livesGroup = self.newGame.livesGroup
        self.heartsGroup = self.newGame.heartsGroup

    def getScore(self, index):
        if index == 1:
            return self.newGame.p1_lives
        if index == 2:
            return self.newGame.p2_lives
        return 21 # error

    def game_over(self):
        return (self.newGame.p1_lives <= 0 or self.newGame.p2_lives <= 0)
    
    #def getGameState(self):
        # implement this

    def step(self, dt):
        # This is where the game is run
        # Get the appropriate groups

        # Animate an object
        #for obj in self.objGroup:
        #    obj.animateObj()

        for event in pygame.event.get():
            # Exit to desktop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                # To check p1 collisions below, we move the player downwards then check
                # and move them back to their original location
                if event.key == self.actions["p1_down"]:
                    if self.newGame.p1_dir != 2:
                        self.newGame.p1_dir = 2
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_down1"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_down2"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[0].update(self.IMAGES["tank_down1"], self.newGame.p1_dir, -self.newGame.Players[0].getSpeed(), 32, 32)
                # To check p1 collisions above, we move the player upwards then check
                # and move them back to their original location
                if event.key == self.actions["p1_up"]:
                    if self.newGame.p1_dir != 0:
                        self.newGame.p1_dir = 0
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_up1"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_up2"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[0].update(self.IMAGES["tank_up1"], self.newGame.p1_dir, -self.newGame.Players[0].getSpeed(), 32, 32)
                # To check p1 collisions right, we move the player to the right, check for collisions,
                # then move them back to their original location
                if event.key == self.actions["p1_right"]:
                    if self.newGame.p1_dir != 1:
                        self.newGame.p1_dir = 1
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_right1"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_right2"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[0].update(self.IMAGES["tank_right1"], self.newGame.p1_dir, -self.newGame.Players[0].getSpeed(), 32, 32)
                # To check p1 collisions left, we move the player to the left, check for collisions,
                # then move them back to their original location
                if event.key == self.actions["p1_left"]:
                    if self.newGame.p1_dir != 3:
                        self.newGame.p1_dir = 3
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_left1"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[0].update(self.IMAGES["tank_left2"], self.newGame.p1_dir, self.newGame.Players[0].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[0].update(self.IMAGES["tank_left1"], self.newGame.p1_dir, -self.newGame.Players[0].getSpeed(), 32, 32)
                        
                # To check p2 collisions below, we move the player downwards then check
                # and move them back to their original location
                if event.key == self.actions["p2_down"]:
                    if self.newGame.p1_dir != 2:
                        self.newGame.p1_dir = 2
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_down1"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_down2"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[1].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[1].update(self.IMAGES["tank_down1"], self.newGame.p1_dir, -self.newGame.Players[1].getSpeed(), 32, 32)
                # To check p2 collisions above, we move the player upwards then check
                # and move them back to their original location
                if event.key == self.actions["p2_up"]:
                    if self.newGame.p1_dir != 0:
                        self.newGame.p1_dir = 0
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_up1"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_up2"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[1].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[1].update(self.IMAGES["tank_up1"], self.newGame.p1_dir, -self.newGame.Players[1].getSpeed(), 32, 32)
                # To check p2 collisions right, we move the player to the right, check for collisions,
                # then move them back to their original location
                if event.key == self.actions["p2_right"]:
                    if self.newGame.p1_dir != 1:
                        self.newGame.p1_dir = 1
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_right1"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_right2"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[1].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[1].update(self.IMAGES["tank_right1"], self.newGame.p1_dir, -self.newGame.Players[1].getSpeed(), 32, 32)
                # To check p2 collisions left, we move the player to the left, check for collisions,
                # then move them back to their original location
                if event.key == self.actions["p2_left"]:
                    if self.newGame.p1_dir != 3:
                        self.newGame.p1_dir = 3
                        self.newGame.cycles = -1  # Reset cycles
                    self.newGame.cycles = (self.newGame.cycles + 1) % 2
                    if self.newGame.cycles == 0:
                        # Display the first image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_left1"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)
                    if self.newGame.cycles == 1:
                        # Display the second image for half the cycles
                        self.newGame.Players[1].update(self.IMAGES["tank_left2"], self.newGame.p1_dir, self.newGame.Players[1].getSpeed(), 32, 32)    
                    self.wallsCollidedExact = self.newGame.Players[1].checkCollision(self.wallGroup)
                    # If we have collided with a wall, move the player back to where it was in the last state
                    if self.wallsCollidedExact:
                        self.newGame.Players[1].update(self.IMAGES["tank_left1"], self.newGame.p1_dir, -self.newGame.Players[1].getSpeed(), 32, 32)
                
                # Check if p1 has fired a shell
                if event.key == self.actions["p1_fire"]:
                    self.newGame.CreateShell(self.newGame.Players[0].getPosition(), self.p1_dir, self.newGame.Players[0].index)
                # Check if p2 has fired a shell
                if event.key == self.actions["p2_fire"]:
                    self.newGame.CreateShell(self.newGame.Players[1].getPosition(), self.p1_dir, self.newGame.Players[1].index)

        # Update the player's position & animation
        #p1_movement = self.newGame.Players[0].continuousUpdate()
        #p2_movement = self.newGame.Players[1].continuousUpdate()

        '''
        We use cycles to animate the character, when we change direction we also reset the cycles
        We also change the direction according to the key pressed
        '''

        # Redraws all our instances onto the screen
        self.newGame.redrawScreen(self.screen, self.width, self.height)

        # Update the shell and check for collisions with the other player
        self.newGame.shellCheck()

        # Check if one player has defeated the other
        self.newGame.checkVictory()
