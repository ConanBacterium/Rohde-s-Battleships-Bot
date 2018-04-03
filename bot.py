from Ship import Ship
from shooter import Shooter
from random import randint
import sys
from random import choice
class BattleshipsBot:
    # Instance variables
    ships = [] # nested list of ships
    allShipCoordinates = [] # list of all the ship coordinates
    enemyShipsSunk = 0
    myShipsSunk = 0
    amountOfShips = 3

    # checks if game is over
    def isGameOver(self):
        if self.enemyShipsSunk == self.amountOfShips or self.myShipsSunk == self.amountOfShips:
            return True
        else:
            return False

    # check if any of the ships have been hit or sunk
    def hitMissOrSunk(self, coords):
        for i in range(0, len(self.ships)): # run through the ships
            if self.ships[i].shootCoord(coords) == True: #check if there's a coordinate match
                if self.ships[i].isSunk() == True: # check if the ship has been sunk
                    return "SUNK" #return "SUNK" if is has
                else: #if not sunk, then just a hit
                    return "HIT"

        return "MISS" #return false if none of the ships had a coordinate match

    # generates coordinates for a ship, and makes sure to neither stack ships nor position them outside the grid.
    def getCoordsForShip(self, size, vertical):
        shipCoords = [] # list holding the coords of the ship

        while 1:
            legit = True # coords are legit, so not stacked on something else, and not outside the grid etc
            startposx = randint(1, 10 - size)  # to make sure that the ship doesn't pass the borders of the grid (should be optimized to consider if the ship is ver or hor)
            startposy = randint(1, 10 - size)  # ^
            coord = ()  # tuple holding the coordinate

            for i in range(0, size):
                if not vertical:  # If the ship should be positioned horizontally
                    startposy = startposy + 1  # Increment of the y position
                elif vertical:
                    startposx = startposx + 1  # Increment of the x position
                coord = (startposx, startposy)  # tuple holding the current coordinate that's being tested

                if coord in self.allShipCoordinates:  # If  coordinates are already used (if stacking ships)
                    legit = False  # Makes sure that the coordinates won't be given to the allShipCoordinations and that the coordinates list will be cleaned
                elif coord not in self.allShipCoordinates:  # If coordinates is not in use (if not stacking ships)
                    shipCoords.append(coord)

            if legit == True:
                for i in shipCoords:
                    self.allShipCoordinates.append(i)  # Puts all the newly given coordinates into the allShipCoordinations
                break  # Get out of the while loop, because none of the coordinates were in use
            elif legit == False:
                del shipCoords[:]  # clean the shipCoords list

        return shipCoords

    # getShips returns a nested list of Ship objects
    def getShips(self, amount):
        ships = []
        for i in range(0, amount):
            #create object of Ship and use the Ship.setIntactShipCoords to pass the object it's coords
            ships.append(
                Ship(self.getCoordsForShip(3+i, choice([True, False])))
            ) # generates a ships that randomly lay vertically or horizontally, and the ships are all 1 coordinate bigger than the previous, the first being 3 coordinates long.
        return ships

    def brain(self):
        shooter = Shooter()
        gameOver = False
        self.ships = self.getShips(self.amountOfShips) #places ships
        print(self.allShipCoordinates)
        while (not gameOver):
            #Bots turn
            print("My turn!")
            if not shooter.currentTarget: # if currentTarget is empty, meaning that ship hasn't been located
                coords = shooter.getRandomCoords()
                self.sendShootingCoordinatesToOpponent(coords)
                print("HIT, MISS OR SUNK?")
                answer = self.getOpponentResponse()
                if answer == "MISS":
                    shooter.missed.append(coords)
                elif answer == "HIT":
                    shooter.hits.append(coords)
                    shooter.currentTarget.append(coords)
                elif answer == "SUNK":
                    self.enemyShipsSunk += 1
                    shooter.hits.append(coords)
                    shooter.reset()
            else: #if currentTarget isn't empty, meaning that ship has been located
                coords = shooter.getTargetCoords(shooter.shootingDirection, shooter.currentTarget[-1])
                self.sendShootingCoordinatesToOpponent(coords)
                answer = self.getOpponentResponse()
                if answer == "MISS" and len(shooter.currentTarget) == 1: #if there's only been one hit, meaning that the bot is finding out if the ship lays vertically or not
                    shooter.missed.append(coords)
                    shooter.changeDirection() #update shootingDirection
                elif answer == "MISS" and len(shooter.currentTarget) > 1: #if there's been more than one hit, meaning that the bot is shooting directly at the ship and has now found the end of it
                    if shooter.endOfShipReached == True: #if the end of the ship has already been reached, then this is the second time, and something is wrong, since both ends have been found but there's been no SUNK
                        print("END OF SHIP HAS BEEN FOUND TWICE, SOMETHING IS WRONG!!!!!!!!")
                        sys.exit()
                    else: #if this is the first time the end of the ship has been reached
                        shooter.endOfShipReached = True
                    shooter.missed.append(coords)
                    shooter.currentTarget = list(reversed(shooter.currentTarget)) #reverse currentTarget so that next time the bot will shoot from the other end
                    shooter.reverseDirection() #reverse the shooting direction so that next time the bot will shoot in the other direction
                elif answer == "HIT":
                    shooter.hits.append(coords)
                    shooter.currentTarget.append(coords)
                elif answer == "SUNK":
                    self.enemyShipsSunk += 1
                    shooter.hits.append(coords)
                    shooter.reset()
            #Bots turn ends, check for game over
            gameOver = self.isGameOver()
            if gameOver == True:
                print("I WIN!")
                break
            #Opponents turn
            print("Your turn. Send coords: x,y")
            opcoords = self.getOpponentCoords()
            botAnswer = self.hitMissOrSunk(opcoords)
            if botAnswer == "SUNK":
                self.myShipsSunk += 1
            print(botAnswer)
            #Opponents turn end, check for game over
            gameOver = self.isGameOver()
            if gameOver == True:
                print("I LOSE!")
                break



        print("GAME IS OVER")



    def sendShootingCoordinatesToOpponent(self, coords):
        print(coords)

    def getOpponentCoords(self):
        coords = input(">")
        coords = coords.split(",") #splitting the string
        coords = (int(coords[0]), int(coords[1])) #creating the tuple and casting from string to int
        return coords

    def getOpponentResponse(self):
        return input(">")
#test area


bot = BattleshipsBot()
bot.brain()
