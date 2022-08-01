import pygame
import math
import sys
import os

from .person import Person
from .environment import Environment
from .player import Player
from .shell import Shell
from .wall import Wall

class Board(object):
    '''
    This class defines our gameboard.
    A gameboard contains everthing related to our game, like the tanks, shells, walls, etc.
    The generation of the level also happens in this class.
    '''

    def __init__(self, width, height, value, lives):
        self.__width = width
        self.__height = height # + 10
        self.value = value # Shell speed
        self.lives = lives
        self.p1_lives = self.lives
        self.p2_lives = self.lives
        self.cycles = 0 # For the tank animations
        self.p1_dir = 1 # player1 is on the left, facing right
        self.p2_dir = 3 # player2 is on the right, facing left

        self.IMAGES = {
            "tank_left1": pygame.image.load(os.path.join(_dir, 'assets/tank_left1.png')).convert_alpha(),
            "tank_right1": pygame.image.load(os.path.join(_dir, 'assets/tank_right1.png')).convert_alpha(),
            "wood_block": pygame.image.load(os.path.join(_dir, 'assets/wood_block.png')).convert_alpha(),
            "lives": pygame.image.load(os.path.join(_dir, 'assets/lives.png')).convert_alpha(),
            "heart": pygame.image.load(os.path.join(_dir, 'assets/heart.png')).convert_alpha(),
            "shell_right2": pygame.image.load(os.path.join(_dir, 'assets/shell_right2.png')).convert_alpha(),
            "shell_left2": pygame.image.load(os.path.join(_dir, 'assets/shell_left2.png')).convert_alpha(),
            "shell_up2": pygame.image.load(os.path.join(_dir, 'assets/shell_up2.png')).convert_alpha(),
            "shell_down2": pygame.image.load(os.path.join(_dir, 'assets/shell_down2.png')).convert_alpha(),
            "shell_down2": pygame.image.load(os.path.join(_dir, 'assets/shell_down2.png')).convert_alpha()
        }

        self.white = (255, 255, 255)

        # The map is an array of 11x11 in which we store what each block on our map is.
        # 1 represents a wall, 2 is a tank, 3 is a bullet, 4 is the lives, 5 is the hearts.
        self.map = []
        # These are the arrays in which we store our instances of different classes
        self.Players = [None] * 2
        self.Walls = []
        self.Shells = [None] * 2
        self.Lives = [None] * 2
        self.Hearts = [None] * 6

        # Resets the above groups and initializes the game for us
        self.resetGroups()

        # Initialize the instance groups which we use to display our instances on the screen
        self.shellGroup = pygame.sprite.RenderPlain(self.Shells)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.livesGroup = pygame.sprite.RenderPlain(self.Lives)
        self.heartsGroup = pygame.sprite.RenderPlain(self.Hearts)

    def resetGroups(self):
        self.cycles = 0 # For the tank animations
        self.p1_dir = 1 # player1 is on the left, facing right
        self.p2_dir = 3 # player2 is on the right, facing left
        self.p1_lives = self.lives
        self.p2_lives = self.lives
        self.map = []  # We will create the map again when we reset the game
        self.Players = [
            Player(self.IMAGES["tank_right1"], (0, int(self.__height / 2)), 32, 32, 1),
            Player(self.IMAGES["tank_left1"], (self.__width - 32, int(self.__height / 2)), 32, 32, 2)]
        self.Walls = []
        self.Shells = []
        self.Lives = [
            Wall(self.IMAGES[lives], 32, 0, 32, 32]), # For player1
            Wall(self.IMAGES[lives], self.__width - 32, 0, 32, 32]) # For player2
        self.Hearts = [
            Wall(self.IMAGES[lives], 32, 0, 32, 32), # player1 life1
            Wall(self.IMAGES[lives], 64, 0, 32, 32), # player1 life2
            Wall(self.IMAGES[lives], 96, 0, 32, 32]), # player1 life3
            Wall(self.IMAGES[lives], self.__width - 64, 0, 32, 32]), # player2 life1
            Wall(self.IMAGES[lives], self.__width - 96, 0, 32, 32]), # player2 life2
            Wall(self.IMAGES[lives], self.__width - 128, 0, 32, 32]) # player2 life3
        self.initializeGame()  # This initializes the game and generates our map
        self.createGroups()  # This creates the instance groups

    # Checks to destroy a shell when it hits a walll or person
    def checkShellDestroy(self, shell, index):
        if pygame.sprite.spritecollide(shell, self.playerGroup[index-1], False) or pygame.sprite.spritecollide(shell, self.wallGroup, False):
            # We can use indices on shells to uniquely identify each shell
            self.DestroyShell(index)

    # Creates a new shell and add it to our shell group
    def CreateShell(self, location, direction, playerIndex):
        # Check if player already has a shell on the board
        if self.Shells[playerIndex-1] == None:
            if direction == 0: # UP
                self.Shells[playerIndex-1](Shell(self.IMAGES["shell_up2"], (location[0], location[1]-32), self.value, direction))
            if direction == 1: # RIGHT
                self.Shells[playerIndex-1](Shell(self.IMAGES["shell_right2"], (location[0]+32, location[1]), self.value, direction))
            if direction == 2: # DOWN
                self.Shells[playerIndex-1](Shell(self.IMAGES["shell_down2"], (location[0], location[1]+32), self.value, direction))
            if direction == 3: # LEFT
                self.Shells[playerIndex-1](Shell(self.IMAGES["shell_left2"], (location[0]-32, location[1]), self.value, direction))
            self.createGroups()  # We recreate the groups so the shell is added
            
    # Destroy a shell if it has collided with a player or hit a wall
    def DestroyShell(self, playerIndex):
        if playerIndex == 1:
            self.Shells[0] = None
        if playerIndex == 2:
            self.Shells[1] = None
        self.createGroups()  # Recreate the groups so the shell is removed
    
    # Remove a heart if the player has lost their life
    def RemoveHeart(self, playerIndex):
        if playerIndex = 1:
            self.p1_lives -= 1
            self.Hearts[0:3] = 0
            for i in range (0, self.p1_lives):
                self.Hearts[i] = 5 # a heart
        if playerIndex = 2:
            self.p2_lives -= 1
            self.Hearts[3:6] = 0
            for i in range (3, self.p1_lives):
                self.Hearts[i] = 5 # a heart
        self.createGroups()  # Recreate the groups so the shell is removed

    # Create an empty 2D map of 11x11 size
    def makeMap(self):
        for point in range(int(self.__height / 32)):
            row = []
            for point2 in range(0, int(self.__width / 32)):
                row.append(0)
            self.map.append(row)

    # Add walls to our map
    def makeWalls(self):
        for i in range(int(self.__height / 32)):
            self.map[i][0] = self.map[i][int(self.__width / 32)] = 1
        for j in range(int(self.__width / 32)):
            self.map[0][j] = self.map[int(self.__width / 32)][j] = 1
    
    # Add hearts to our map
    def makeHearts(self):
        for i in range(3):
            self.map[0][i] = self.map[0][i] = 5
            self.map[0][int(self.__width / 32) - j - 1] = self.map[0][int(self.__width / 32) - i - 1] = 5

    '''
    This is called once you have finished making the game field
    You use the 2D map to add instances to the groups
    '''
    def populateMap(self):
        hearts = 0
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    # Add a wall at that position
                    self.Walls.append(OnBoard(self.IMAGES["wood_block"],(x * 32, y * 32)))
                elif self.map[x][y] == 5:
                    # Add the hearts at their position
                    self.Hearts[hearts] = OnBoard(self.IMAGES["hearts"],(x * 32, y * 32))
                    hearts += 1

    # Update all the shell positions and check for collisions with players
    def shellCheck(self):
        for i in range(len(self.shellGroup)):
            self.shellGroup[i].continuousUpdate(self.wallGroup)
            if i == 0 and shell.checkCollision(self.playerGroup[1]):
                self.shell[0] = 0
                self.Players[1].setPosition((self.__width - 32, int(self.__height / 2)))
                self.p2_lives -= 1
                self.createGroups()
            if i == 1 and shell.checkCollision(self.playerGroup[0]):
                self.shell[1] = 0
                self.Players[0].setPosition((0, int(self.__height / 2)))
                self.p1_lives -= 1
                self.createGroups()
            self.checkShellDestroy(Shell, 1)
            self.checkShellDestroy(Shell, 2)

    # Check if the player wins
    def checkVictory(self):
        if self.p1_lives <= 0:
            print("Player 2 (right) wins!")
        if self.p2_lives <= 0:
            print("Player 1 (left) wins!")    
        self.resetGroups()

    # Redraws the entire game screen
    def redrawScreen(self, screen, width, height):
        #screen.blit(self.background_image, (0, 0))
        #self.backdrop.draw_background(self.screen) 
        screen.fill((130, 90, 60))  # Fill it with brown
        # Draw all our groups on the background
        self.shellGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.wallGroup.draw(screen)
        self.livesGroup.draw(screen)
        self.heartsGroup.draw(screen)

    # Update all the groups from their corresponding lists
    def createGroups(self):
        self.shellGroup = pygame.sprite.RenderPlain(self.Shells)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.livesGroup = pygame.sprite.RenderPlain(self.Lives)
        self.heartsGroup = pygame.sprite.RenderPlain(self.Hearts)

    '''
    Initialize the game by making the map, generating walls, and updating the groups.
    '''
    def initializeGame(self):
        self.makeMap()
        self.makeWalls()
        self.makeHearts()
        self.populateMap()
        self.createGroups()
