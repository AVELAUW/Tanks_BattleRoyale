import pygame

'''
This class defines all of the 'living' objects in the game (e.g. player1 and player2)
Each of these objects can move in any direction specified.
'''


class Person(pygame.sprite.Sprite):

    def __init__(self, raw_image, position, width, height, index):
        super(Person, self).__init__()
        self.width = width
        self.height = height
        self.index = index
        self.__position = position
        self.image = raw_image
        self.image = pygame.transform.scale(
            self.image, (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    '''
    We set these as abstract methods since this class does not have a speed variable set, but we want all the child classes to
    set a movement speed and they should have setters and getters for this movement speed.
    '''

    def getSpeed(self):  # Abstract method
        raise NotImplementedError("Subclass must implement this")

    def setSpeed(self):  # Abstract method
        raise NotImplementedError("Subclass must implement this")

    # Getters and Setters
    def setCenter(self, position):
        self.rect.center = position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    # Move the person in the horizontal (%2==1) or vertical (%2==0) axis
    def update(self, raw_image, direction, value, width, height):
        if direction == 0: # UP
            self.__position = (self.__position[0], self.__position[1] - value)
        if direction == 1: # RIGHT
            self.__position = (self.__position[0] + value, self.__position[1])
        if direction == 2: # DOWN
            self.__position = (self.__position[0], self.__position[1] + value)
        if direction == 3: # LEFT
            self.__position = (self.__position[0] - value, self.__position[1])
        # Update the image to the specified width and height
        self.image = pygame.transform.scale(self.image, (width, height))    
        self.rect.center = self.__position

    # Given a collider list, just check if the person instance collides with
    # any of them
    def checkCollision(self, colliderGroup):
        Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
        return Colliders

    # This is another abstract function, and it must be implemented in child
    # classes inheriting from this class
    def continuousUpdate(self, GroupList, GroupList2):
        # continuousUpdate that gets called frequently for collision checks,
        # movement etc
        raise NotImplementedError("Subclass must implement this")
