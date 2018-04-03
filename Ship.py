#CLASS FOR THE SHIPS

class Ship:
    # Instance variables
    intactShipCoords = [] # list of the ship coordinates that haven't been shot at
    damagedShipCoords = [] # list of the ship coordinates that have been shot at


    def __init__(self, shipCoords):
        self.intactShipCoords = shipCoords

    def isSunk(self):
        if not self.intactShipCoords: #if intactShipCoords is empty
            return True
        else:
            return False

    # Check if given coordinate matches a coordinate in intactShipCoords and if it does, move coord from intactShipCoords to damagedShipCoords and return true, else return false
    def shootCoord(self, coords):
        # iterate through intactShipCoords, check if match, if match, remove from intactShipCoords and append to damagedShipCoords, and return True, else return False
        for coord in self.intactShipCoords:
            if coord == coords:
                self.intactShipCoords.remove(coord)
                self.damagedShipCoords.append(coord)
                return True

        return False

    # Self explanatory  THIS ONLY RETURNS THE INTACTSHIPCOORDS !!!!!
    def getShipCoords(self):
        return self.intactShipCoords # THIS ONLY RETURNS THE INTACTSHIPCOORDS

    # clear the lists of ship coordinates (damaged and intact) to ready for a new game
    def clearShipCoords(self):
        self.intactShipCoords = [] # clear it
        self.damagedShipCoords = [] #clear it
        self.sunk = True

    # Self explanatory. Expects a list of x,y int tuples.
    def setShipCoords(self, coords):
        # self explanatory
        self.intactShipCoords = coords