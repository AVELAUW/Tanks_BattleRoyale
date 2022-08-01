from .person import Person

'''
This class defines our tanks players.
It inherits from the Person class.
'''


class Player(Person):
    def __init__(self, raw_image, position, width, height, index):
        super(Player, self).__init__(raw_image, position, width, height, index)
        self.index = index
        self.__speed = 5  # Movement speed of the player

    # Getters and Setters
    def getSpeed(self):
        return self.__speed

    def setSpeed(self):
        return self.__speed

    # This manages the players shell
    def continuousUpdate(self, wallGroupList):
        # Only run when the player has no shell on the map
        
        if self.onLadder == 0:
            wallsCollided = self.checkCollision(wallGroupList)

            # If the player is not jumping
            if self.isJumping == 0:
                # We move down a little and check if we collide with anything
                self.updateY(2)
                laddersCollided = self.checkCollision(ladderGroupList)
                wallsCollided = self.checkCollision(wallGroupList)
                self.updateY(-2)
                # If we are not colliding with anything below, then we start a
                # jump with 0 speed so that we just fall down
                if len(wallsCollided) == 0 and len(laddersCollided) == 0:
                    self.isJumping = 1
                    self.currentJumpSpeed = 0
