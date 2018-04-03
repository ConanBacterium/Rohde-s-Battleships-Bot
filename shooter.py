from random import randint
import sys

class Shooter:
    missed = [] #all misses
    hits = [] #all hits
    currentTarget = [] #coordinates that's been shot on the ship that's currently being targeted
    endOfShipReached = False #if target has been shot multiple times but suddenly there's a MISS, then the end of the ship is reached and bot must shoot at the other end
    multipleShips = False #if  multiple ships lay besides eachother, and bot has been shooting across them all.
    shootingDirection = 0 # 0 means shoot to the right, 1 means up, 2 left, 3 down, 4 means something is wrong since all directions has been shot

    # reset after a ship has been sunk
    def reset(self):
        self.currentTarget[:] = []
        self.endOfShipReached = False
        self.multipleShips = False
        self.shootingDirection = 0

    # function for increasing the shootingDirection
    def changeDirection(self):
        if self.shootingDirection is not 3:
            self.shootingDirection += 1
        elif self.shootingDirection is 3:
            print("HAS SHOT IN ALL DIRECTIONS SOMETHING IS WRONG!!!!")
            sys.exit()

    # function for reversing the shootingDirection
    def reverseDirection(self):
        if self.shootingDirection == 0:
            self.shootingDirection = 2
        elif self.shootingDirection == 1:
            self.shootingDirection = 3
        elif self.shootingDirection == 2:
            self.shootingDirection = 0
        elif self.shootingDirection == 3:
            self.shootingDirection = 1

    # self explanatory
    def isPrevTargeted(self, coords):
        if coords in self.hits or coords in self.missed:
            return True
        else:
            return False

    def getRandomCoords(self):
        targetCoords = (randint(1,10), randint(1,10))
        if targetCoords in self.hits or targetCoords in self.missed:
            targetCoords = self.getRandomCoords()
        return targetCoords

    def getTargetCoords(self, direction, prevCoords):
        if direction == 0: #shoot to the right
            targetCoords = self.getRightCoords(prevCoords)
        elif direction == 1: #shoot above
            targetCoords = self.getAboveCoords(prevCoords)
        elif direction == 2: #shoot left
            targetCoords = self.getLeftCoords(prevCoords)
        elif direction == 3: #shoot below
            targetCoords = self.getBelowCoords(prevCoords)
        return targetCoords


    #function for getting the coordinates to the left of referenceCoords
    def getLeftCoords(self, referenceCoords):
        return (referenceCoords[0]-1, referenceCoords[1]) # decrease x and return

    #function for getting the coordinates to the right of referenceCoords
    def getRightCoords(self, referenceCoords):
        return (referenceCoords[0]+1, referenceCoords[1])

    # function for getting the coordinates above referenceCoords
    def getAboveCoords(self, referenceCoords):
        return (referenceCoords[0], referenceCoords[1]-1)

    # function for getting the coordinates below referenceCoords
    def getBelowCoords(self, referenceCoords):
        return (referenceCoords[0], referenceCoords[1] + 1)