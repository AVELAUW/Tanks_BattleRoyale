from .person import Person

'''
This class defines our tanks players.
It inherits from the Person class.
'''


class Player(Person):
    def __init__(self, raw_image, position, width, height, index):
        super(Player, self).__init__(raw_image, position, width, height)
        self.index = index
        self.__speed = 3  # Movement speed of the player

    # Getters and Setters
    def getSpeed(self):
        return self.__speed

    def setSpeed(self):
        return self.__speed

    # The tank does not move without an event
    def continuousUpdate(self):
        print("sitting still")
        return none
