import pygame
import math
import sys
import os

from .person import Person
from .environment import Environment
from .player1 import Player1
from .player2 import Player2
from .shell import Shell
from .wall import Wall

class Board(object):
    '''
    This class defines our gameboard.
    A gameboard contains everthing related to our game, like the tanks, shells, walls, etc.
    The generation of the level also happens in this class.
    '''

    def __init__(self, width, height, rewards, value, lives):
        self.__width = width
        self.__height = height # + 10
        self.value = value # Shell speed
        self.lives = lives
        self.p1_lives = self.lives
        self.p2_lives = self.lives
        self.rewards = rewards
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

        # Initialize the instance groups which we use to display our instances
        # on the screen
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
            Player1(self.IMAGES["tank_left1"], (1, int(self.__height / 2)), 32, 32),
            Player2(self.IMAGES["tank_left1"], (self.__width - 33, int(self.__height / 2)), 32, 32)]
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

    # Checks to destroy a shell when it reaches its terminal point
    def checkShellDestroy(self, shell):
        if pygame.sprite.spritecollide(shell, self.playerGroup, False):
            # We use indices on shells to uniquely identify each shell
            self.DestroyShell(shell.index)

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

    # Destroy a shell if it has collided with a player or hit a wall
    def DestroyShell(self, playerIndex):
        if playerIndex == 1:
            self.Shells[0] = None
        if playerIndex == 2:
            self.Shells[1] = None
        self.createGroups()  # Recreate the groups so the shell is removed

    # Create an empty 2D map of 11x11 size
    def makeMap(self):
        for point in range(int(self.__height / 32)):
            row = []
            for point2 in range(0, int(self.__width / 32)):
                row.append(0)
            self.map.append(row)

    # Add walls to our map boundaries
    def makeWalls(self):
        for i in range(int(self.__height / 32)):
            self.map[i][0] = self.map[i][int(self.__width / 32)] = 1
        for j in range(int(self.__width / 32)):
            self.map[0][j] = self.map[int(self.__width / 32)][j] = 1

    '''
    This is called once you have finished making the game field
    You use the 2D map to add instances to the groups
    '''
    def populateMap(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    # Add a wall at that position
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 2:
                    # Add a ladder at that position
                    self.Ladders.append(
                        OnBoard(
                            self.IMAGES["ladder"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))

    # Update all the fireball positions and check for collisions with player
    def fireballCheck(self):
        for fireball in self.fireballGroup:
            fireball.continuousUpdate(self.wallGroup, self.ladderGroup)
            if fireball.checkCollision(self.playerGroup, "V"):
                self.Fireballs.remove(fireball)
                self.Players[0].setPosition((50, 440))
                self.score += self.rewards["negative"]
                self.lives += -1
                self.createGroups()
            self.checkFireballDestroy(fireball)

    # Check for coins collided and add the appropriate score
    def coinCheck(self, coinsCollected):
        for coin in coinsCollected:
            self.score += self.rewards["positive"]
            # We also remove the coin entry from our map
            self.map[int((coin.getPosition()[1] - 15 / 2) /
                     15)][int((coin.getPosition()[0] - 15 / 2) / 15)] = 0
            # Remove the coin entry from our list
            self.Coins.remove(coin)
            # Update the coin group since we modified the coin list
            self.createGroups()

    # Check if the player wins
    def checkVictory(self):
        # If you touch the princess or reach the floor with the princess you
        # win!
        if self.Players[0].checkCollision(self.allyGroup) or self.Players[
                0].getPosition()[1] < 4 * 15:

            self.score += self.rewards["win"]

            # This is just the next level so we only clear the fireballs and
            # regenerate the coins
            self.Fireballs = []
            self.Players[0].setPosition((50, 440))
            self.Coins = []
            self.GenerateCoins()

            # Add monsters
            if len(self.Enemies) == 1:
                self.Enemies.append(
                    MonsterPerson(
                        self.IMAGES["monster0"], (700, 117), self.rng, self._dir))
            elif len(self.Enemies) == 2:
                self.Enemies.append(
                    MonsterPerson(
                        self.IMAGES["monster0"], (400, 117), self.rng, self._dir))
            # Create the groups again so the enemies are effected
            self.createGroups()

    # Redraws the entire game screen
    def redrawScreen(self, screen, width, height):
        screen.fill((40, 20, 0))  # Fill it with black
        # Draw all our groups on the background
        self.ladderGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.coinGroup.draw(screen)
        self.wallGroup.draw(screen)
        self.fireballGroup.draw(screen)
        self.enemyGroup.draw(screen)
        self.allyGroup.draw(screen)

    # Update all the groups from their corresponding lists
    def createGroups(self):
        self.fireballGroup = pygame.sprite.RenderPlain(self.Fireballs)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.enemyGroup = pygame.sprite.RenderPlain(self.Enemies)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)
        self.fireballEndpointsGroup = pygame.sprite.RenderPlain(
            self.FireballEndpoints)

    '''
    Initialize the game by making the map, generating walls, generating princess chamber, generating ladders randomly,
    generating broken ladders randomly, generating holes, generating coins randomly, adding the ladders and walls to our lists
    and finally updating the groups.
    '''

    def initializeGame(self):
        self.makeMap()
        self.makeWalls()
        self.makePrincessChamber()
        self.makeLadders()
        self.makeHoles()
        self.GenerateCoins()
        self.populateMap()
        self.createGroups()
