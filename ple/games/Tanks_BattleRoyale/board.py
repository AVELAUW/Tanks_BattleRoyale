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

    def __init__(self, width, height, value, _dir):
        self.__width = width
        self.__height = height
        self.adjust = 14
        self.value = value # value # Shell speed
        self.life = 3
        self.p1_lives = self.life
        self.p2_lives = self.life
        self.cycles = 0 # For the tank animations
        self.p1_dir = 1 # player1 is on the left, facing right
        self.p2_dir = 3 # player2 is on the right, facing left
        
        #self._dir = _dir
        self._dir = os.path.dirname(os.path.abspath(__file__))
        self.LIVES1 = [511, 512, 513]
        self.LIVES2 = [521, 522, 523]
        self.IMAGES = {
            "tank_left1": pygame.image.load(os.path.join(self._dir, 'assets/tank_left_1.png')).convert_alpha(),
            "tank_right1": pygame.image.load(os.path.join(self._dir, 'assets/tank_right_1.png')).convert_alpha(),
            "tank_down1": pygame.image.load(os.path.join(self._dir, 'assets/tank_down_1.png')).convert_alpha(),
            "tank_up1": pygame.image.load(os.path.join(self._dir, 'assets/tank_up1.png')).convert_alpha(),
            "wood_block": pygame.image.load(os.path.join(self._dir, 'assets/wood_block.png')).convert_alpha(),
            "lives": pygame.image.load(os.path.join(self._dir, 'assets/lives.png')).convert_alpha(),
            "heart": pygame.image.load(os.path.join(self._dir, 'assets/heart.png')).convert_alpha(),
            "shell_right2": pygame.image.load(os.path.join(self._dir, 'assets/shell_right2.png')).convert_alpha(),
            "shell_left2": pygame.image.load(os.path.join(self._dir, 'assets/shell_left2.png')).convert_alpha(),
            "shell_up2": pygame.image.load(os.path.join(self._dir, 'assets/shell_up_2.png')).convert_alpha(),
            "shell_down2": pygame.image.load(os.path.join(self._dir, 'assets/shell_down2.png')).convert_alpha(),
            "boom3": pygame.transform.scale(pygame.image.load(os.path.join(self._dir, 'assets/boom3.png')), (32, 32)).convert_alpha(),
            "background1": pygame.transform.scale(pygame.image.load(os.path.join(self._dir, 'assets/dirt.png')), (352, 352)).convert_alpha(),
            "background2": pygame.transform.scale(pygame.image.load(os.path.join(self._dir, 'assets/dirt2.png')), (352, 352)).convert_alpha()
        }

        self.white = (255, 255, 255)

        # The map is an array of 11x11 in which we store what each block on our map is.
        # 1 represents a wall, 2 is a tank, 3 is a bullet, 4 is the lives, 5 is the hearts.
        self.map = []
        # These are the arrays in which we store our instances of different classes
        self.Players = []
        self.Walls = []
        self.Shells = []
        self.Lives = []
        self.Hearts = []
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
        self.p1_lives = self.life
        self.p2_lives = self.life
        self.map = []  # We will create the map again when we reset the game
        self.Players = [
            Player(self.IMAGES["tank_right1"], (32+self.adjust, int(self.__height / 2)), 32, 32, 1),
            Player(self.IMAGES["tank_left1"], (self.__width - 64+self.adjust, int(self.__height / 2)), 32, 32, 2)]
        self.Walls = []
        self.Shells = []
        self.Lives = [
            Wall(self.IMAGES["lives"], (32, self.adjust), 41), # For player1
            Wall(self.IMAGES["lives"], (self.__width - 128-self.adjust, self.adjust), 42)] # For player2
        #for playa in self.Lives: playa.modifySize(self.IMAGES[lives], 32, 96)
        self.Hearts = [
            Wall(self.IMAGES["heart"], (64, self.adjust), 511), # player1 life1
            Wall(self.IMAGES["heart"], (96, self.adjust), 512), # player1 life2
            Wall(self.IMAGES["heart"], (128, self.adjust), 513), # player1 life3
            Wall(self.IMAGES["heart"], (self.__width - 32-self.adjust, self.adjust), 521), # player2 life1
            Wall(self.IMAGES["heart"], (self.__width - 64-self.adjust, self.adjust), 522), # player2 life2
            Wall(self.IMAGES["heart"], (self.__width - 96-self.adjust, self.adjust), 523)] # player2 life3
        self.initializeGame()  # This initializes the game and generates our map
        self.createGroups()  # This creates the instance groups

    # Checks to destroy a shell when it hits a walll or person
    def checkShellDestroy(self, shell):
        if pygame.sprite.spritecollide(shell, self.playerGroup, False) or pygame.sprite.spritecollide(shell, self.wallGroup, False):
            shell.update(self.IMAGES["boom3"],self.value)
            # We can use indices on shells to uniquely identify each shell
            self.DestroyShell(shell.index)

    # Creates a new shell and add it to our shell group
    def CreateShell(self, location, direction, playerIndex):
        # Check if player already has a shell on the board
        shoot = True
        for shell in range(len(self.Shells)):
            if self.Shells[shell].index == playerIndex:
                shoot = False
        if shoot:
            if direction == 0: # UP
                self.Shells.append(Shell(self.IMAGES["shell_up2"], (location[0],location[1]-32), self.value, direction, playerIndex))               
            if direction == 1: # RIGHT
                self.Shells.append(Shell(self.IMAGES["shell_right2"], (location[0]+32, location[1]), self.value, direction, playerIndex))
            if direction == 2: # DOWN
                self.Shells.append(Shell(self.IMAGES["shell_down2"], (location[0], location[1]+32), self.value, direction, playerIndex))
            if direction == 3: # LEFT
                self.Shells.append(Shell(self.IMAGES["shell_left2"], (location[0]-32, location[1]), self.value, direction, playerIndex))
            self.createGroups()  # We recreate the groups so the shell is added
            
    # Destroy a shell if it has collided with a player or hit a wall
    def DestroyShell(self, playerIndex):
        for shell in range(len(self.Shells)):
            if self.Shells[shell].index == playerIndex:
                self.Shells.remove(self.Shells[shell])
                break
        self.createGroups()  # Recreate the groups so the shell is removed
    
    # Remove a heart if the player has lost their life
    def RemoveHeart(self, playerIndex):
        print(len(self.Hearts))
        if playerIndex == 1:
            for heart in range(len(self.Hearts)):
                if self.Hearts[heart].index == self.LIVES1[self.p1_lives-1]:
                    self.Hearts.remove(self.Hearts[heart]) 
                    self.p1_lives -= 1
                    print("Player 1 RemoveHeart", self.p1_lives)
                    break
        elif playerIndex == 2:
            for heart in range(len(self.Hearts)):
                if self.Hearts[heart].index == self.LIVES2[self.p2_lives-1]:
                    self.Hearts.remove(self.Hearts[heart]) 
                    self.p2_lives -= 1
                    print("Player 2 RemoveHeart",self.p2_lives)
                    break
        self.createGroups()  # Recreate the groups so the shell is removed
        print(len(self.Hearts))

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
            self.map[i][0] = 1
            self.map[i][int(self.__width / 32) - 1] = 1
        for j in range(int(self.__width / 32)):
            self.map[0][j] = 1
            self.map[int(self.__width / 32) - 1][j] = 1
        # Block center of map
        self.map[5][2] = 1
        self.map[5][5] = 1
        self.map[5][8] = 1

    '''
    This is called once you have finished making the game field
    You use the 2D map to add instances to the groups
    '''
    def populateMap(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    # Add a wall at that position
                    self.Walls.append(Environment(self.IMAGES["wood_block"],(x * 32+self.adjust, y * 32+self.adjust)))
                #elif self.map[x][y] == 5:
                    # Add the hearts at their position
                    #self.Hearts.append(Environment(self.IMAGES["heart"],(x * 32, y * 32))

    # Update all the shell positions and check for collisions with players
    def shellCheck(self):
        for shell in self.shellGroup:
            shell.continuousUpdate(self.wallGroup, self.playerGroup)
            if shell.index == 1 and shell.checkCollision(self.playerGroup):
                self.Shells.remove(shell)
                self.Players[1].setPosition((32+self.adjust, int(self.__height / 2)))
                self.RemoveHeart(2) # Player 2 hit
                self.createGroups()
            if shell.index == 2 and shell.checkCollision(self.playerGroup):
                self.Shells.remove(shell)
                self.Players[0].setPosition((self.__width - 64+self.adjust, int(self.__height / 2)))
                self.RemoveHeart(1) # Player 1 hit
                self.createGroups()
            self.checkShellDestroy(shell)
    
    # Check if the player wins
    def checkVictory(self):
        if self.p1_lives <= 0:
            print("Player 2 (right) wins!")
            self.resetGroups()
        if self.p2_lives <= 0:
            print("Player 1 (left) wins!")    
            self.resetGroups()

    # Redraws the entire game screen
    def redrawScreen(self, screen, width, height):
        #self.backdrop.draw_background(self.screen) 
        screen.blit(self.IMAGES["background1"], (0, 0))
        #screen.fill((130, 90, 60))  # Fill it with brown
        # Draw all our groups on the background
        self.wallGroup.draw(screen)
        self.livesGroup.draw(screen)
        #self.heartsGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.shellGroup.draw(screen)

    # Update all the groups from their corresponding lists
    def createGroups(self):
        self.shellGroup = pygame.sprite.RenderPlain(self.Shells)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.livesGroup = pygame.sprite.RenderPlain(self.Lives)
        self.heartsGroup = pygame.sprite.RenderPlain(self.Hearts)
        print(len(self.heartsGroup))

    '''
    Initialize the game by making the map, generating walls, and updating the groups.
    '''
    def initializeGame(self):
        self.makeMap()
        self.makeWalls()
        self.populateMap()
        self.createGroups()
