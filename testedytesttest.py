from random import randint

class Test():
    ships = [] #five ships are to be contained 'ere - this haz 2 be a nested list
    allShipCoordinates = [] #holds the coordinates to all the ships - used when positioning ships, by iterating this list the bot can make sure not to stack ships

    def getShips(self):
        ships = [
            self.getCoordinatesToPlaceShip(2, randint(1,10)), # size of ship 2
            self.getCoordinatesToPlaceShip(2, randint(1,10)),# size of ship 2
            self.getCoordinatesToPlaceShip(3, randint(1,10)),# size of ship 3
            self.getCoordinatesToPlaceShip(3, randint(1,10)),# size of ship 3
            self.getCoordinatesToPlaceShip(5, randint(1,10))# size of ship 5
        ]
        return ships

    def getCoordinatesToPlaceShip(self, size, verOrHor):
        coordinates = [] #list for the coordinates
        while 1:
            legit = True
            startposx = randint(1, 10 - size) # to make sure that the ship doesn't pass the borders of the grid (should be optimized to consider if the ship is ver or hor)
            startposy = randint(1, 10 - size) # ^

            theCoordinate = str(startposx) + "," + str(
                startposy)  # string holding the current coordinate that's being tested
            for i in range(0, size):
                if verOrHor % 2 == 0:  # If the ship should be positioned horizontally
                    theCoordinate = str(startposx) + "," + str(startposy + i)  # Increment of the y position
                elif verOrHor % 2 != 0:
                    theCoordinate = str(startposx + i) + "," + str(startposy)  # Increment of the x position

                if theCoordinate in self.allShipCoordinates:  # If theCoordinate is already used
                    legit = False  # Makes sure that the coordinates won't be given to the alLShipCoordinations and that the coordinates list will be cleaned
                elif theCoordinate not in self.allShipCoordinates:  # If theCoordinate is not in use
                    coordinates.append(theCoordinate)  # append theCoordinate

            if legit == True:
                for i in coordinates:
                    self.allShipCoordinates.append(i)  # Puts all the newly given coordinates into the allShipCoordinations
                break  # Get out of the while loop, because none of the coordinates were in use
            elif legit == False:
                del coordinates[:]  # clean the coordinates list
        return coordinates

test = Test()
test.ships = test.getShips()
print test.ships