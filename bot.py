__author__ = 'rohdehoved'
from random import randint
import ircClient as server
class supermegakillerbot:

    codod = 0
    startPoints = [] #holds all the coordinates of starting points of ships that we know of and haven't yet sinked/sunk
    currentShip = [] # holds all the coordinates of the ship that we're attacking
    searchForDirection = 0 #integer used when a ship has been located. Check line underneath:
    # 0 means that we haven't searched any directions yet. 1 means we've shot to the right. 2 means we've tried both the right and the top.
    # 3 means we've tried botht the right, top and the left. 4 means we've shot at the bottom, and then all directions have been tried. Something is
    # wrong then.
    missed = []
    hit = []
    currentTargetCoordinates = ""
    ship1 = [] # 5 blocks
    ship2 = [] # 3 blocks
    ship3 = [] # 3 blocks
    ship4 = [] # 2 blocks
    ship5 = [] # 2 blocks
    allShipCoordinates = []
    losses = 0

    #constructor
    def _init_(self):
        print "_init_ of supermegakillerbot class"
        self.brain()

    #positionShips function (self explanatory) - STATUS: WORKS
    def positionShips(self):
        #global ship1, ship2, ship3, ship4, ship5;
        self.ship1 = self.funnyStuff(5, randint(1,10)) #tells the funnyStuff that the ship1 has to be filled with 2 coordinations (that's the size of the ship)
        self.ship2 = self.funnyStuff(3, randint(1,10)) #Same shit
        self.ship3 = self.funnyStuff(3, randint(1,10)) #^ the randint is to randomize if the ship should be ver or hor, if divisible by 2 it's ver, else hor
        self.ship4 = self.funnyStuff(2, randint(1,10)) #^
        self.ship5 = self.funnyStuff(2, randint(1,10)) #^

    #funnyStuff (I lacked the creativity to find a good name for this function) - STATUS: WORKS
    def funnyStuff(self, sizeOfShip, verOrHor): #ver == divisible by 2, hor == undivisible by 2 #!!"#)!"#!"# RIGHT NOW IT DOESN'T USE THE VERORHOR!! !)"=#!"#)
        #global allShipCoordinates
        coordinates = [] #list for the coordinates

        while 1:
            startPosX = randint(1, 10-sizeOfShip) #to make sure that the ship doesn't pass the borders of the grid (should be optimized to consider if the ship is ver or hor)
            startPosy = randint(1,10-sizeOfShip) #^
            legit = True
            theCoordinate = str(startPosX) + "," + str(startPosy) #string holding the current coordinate that's being tested
            for i in range(0,sizeOfShip):
                if verOrHor % 2 == 0: #If the ship should be positioned horizontally
                    theCoordinate = str(startPosX) + "," + str(startPosy + i) #Increment of the y position
                elif verOrHor % 2 != 0:
                    theCoordinate = str(startPosX + i) + "," + str(startPosy) #Increment of the x position
                if theCoordinate in self.allShipCoordinates: # If theCoordinate is already used
                    legit = False # Makes sure that the coordinates won't be given to the alLShipCoordinations and that the coordinates list will be cleaned
                elif theCoordinate not in self.allShipCoordinates: #If theCoordinate is not in use
                    coordinates.append(theCoordinate) #append theCoordinate

            if legit == True:
                for i in coordinates:
                    self.allShipCoordinates.append(i) #Puts all the newly given coordinates into the allShipCoordinations
                break #Get out of the while loop, because none of the coordinates were in use
            elif legit == False:
                del coordinates[:] #clean the coordinates list
        return coordinates

    #STATUS: WORKS
    def attack(self, codod):
        #global currentTargetCoordinates, searchForDirection
        if codod == 0:
            self.randomShot()
        elif codod == 1:
            self.circleShot()

            while(self.checkIfPrevTarg(self.currentTargetCoordinates) == True):
                self.circleShot()
        elif codod > 1:
            self.directShot()

    #STATUS: WORKS
    def opponentAnswer(self, response):
        #global codod, currentShip, startPoints, searchForDirection, missed, hit, currentTargetCoordinates

        if response == "SUNK":
            self.hit.append(self.currentTargetCoordinates)
            self.codod = 1 # circle shoot
            if self.startPoints: #if startPoints is not empty
                self.startPoints.pop(0) #remove first element

            currentShip = [] #clear currentShip
            if self.startPoints:
                self.currentShip.append(self.startPoints[0]) #append the (new) first element of startPoints.

            searchForDirection = 0 # meaning we haven't found out the direction of the ship yet
            if not self.startPoints: # if startPoints is empty
                self.codod = 0 # no ship has been located, shoot random

        elif response == "MISS":
            self.missed.append(self.currentTargetCoordinates)
            if self.codod == 2:
                self.codod = 3
                # last element of currentShip has to be the same as the new one, because directShot function looks for the last element of currentShip and shoots with that as a reference point, and since we're shooting at the other end now, the reference point is the first place we shot at
                self.currentShip.append(self.currentShip[0])
            elif self.codod == 3: #if several ships laying beside each other has been reached
                self.codod = 1
                startPoints = self.currentShip
                currentShip = []
                currentShip.append(startPoints[0])

        elif response == "HIT":
            self.hit.append(self.currentTargetCoordinates)
            self.currentShip.append(self.currentTargetCoordinates)
            if self.codod == 1:
                self.codod = 2
            elif self.codod == 0:
                self.codod = 1


     # STATUS: WORKS

    def randomShot(self):
        #global currentTargetCoordinates
        self.currentTargetCoordinates = str(randint(1, 10)) + "," + str(randint(1,10)) #get random coordinates
        while self.checkIfPrevTarg(self.currentTargetCoordinates) == True: #as long as the coordinates have been shot at before, try with new coordinates
            self.currentTargetCoordinates = str(randint(1, 10)) + "," + str(randint(1,10)) #get random coordinates

    #STATUS: WORKS - THOUGH YOU HAVE TO MAKE SURE THAT IT DOESN'T SHOOT FOR THE SAME PLACE TWICE
    def circleShot(self):
         #global currentTargetCoordinates, currentShip, searchForDirection
         a = self.currentShip[0].split(",") #currentShip should only contain ONE string/element, as we're supposed to locate the rest of the ship
         temp = [int(a[0]), int(a[1])] #casting from string to int

         if self.searchForDirection == 0: #if we just started searching for the rest of the ship, shoot to the right (increase x)
             temp[0] = temp[0] + 1 #increase x value (shoot to the right)
             self.searchForDirection = 1 # so the bot knows that it has shot to the right
         elif self.searchForDirection == 1: #if we already shot to the right in the search for the rest of the ship, shoot above (decrease y)
             temp[1] = temp[1] - 1
             self.searchForDirection = 2 #so the bot knows that it has shot above
         elif self.searchForDirection == 2: #if we already shot above in the search for the rest of the ship, shoot to the left (decrease x)
             temp[0] = temp[0] - 1
             self.searchForDirection = 3 #so the bot knows it has shot to the left
         elif self.searchForDirection == 3: #if we already shot to the left in the search for the rest of the ship, shoot below (increase y)
             temp[1] = temp[1] + 1
             self.searchForDirection = 4 #so the bot knows it has shot below

         self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1])#Put the new coordinates into the currentTargetCoordinates

    #STATUS: WORKS
    def directShot(self):
        #global searchForDirection, currentTargetCoordinates, codod
        if self.searchForDirection == 1: #if the ship lays horizontally and the bot started shooting to the right
            if self.codod == 3: #if end is reached shoot to the left of the first element
                a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] - 1 #decrease the x value (the first element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

            elif self.codod == 2: #shoot to the right
                 a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                 temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                 temp[0] = temp[0] + 1 #increase the x value (the first element)

                 self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

        elif self.searchForDirection == 2: #if the ship lays vertically, and the bot started shooting above
            if self.codod == 3: #if end is reached shoot below
                a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] + 1 #increase the y value (the second element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

            elif self.codod == 2: #shoot above the last element
                a = self.currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] - 1 #decrease the y value (the second element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

        elif self.searchForDirection == 3: #if the ship lays horizontally, and the bot started shooting to the left
            if self.codod == 3: #if end is reached shoot to the right of the first element
                a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] + 1 #decrease the x value (the second element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates


            elif self.codod == 2: #if end is not reached -  #shoot to the left of the last element
                a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] - 1 #decrease the x value (the second element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

        elif self.searchForDirection == 4: #if the ship lays vertically, and the bot started shooting below
            if self.codod == 3: #if end is reached shoot above the first element
                a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] - 1 #decrease the y value (the second element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

            elif self.codod == 2: #if end is not reached - #shoot below the last element
                a = self.currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] + 1 #decrease the y value (the second element)

                self.currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

    #Function for checking if a coordinate has been targeted before - STATUS: WORKS
    def checkIfPrevTarg(self, coordinates):
        #global missed, hit
        prevTarg = False
        for i in self.missed:
            if coordinates == i: #If the coordinates have already been targeted
               return True
        for i in self.hit:
            if coordinates == i: #If the coordinates have already been targeted
                return True
        return False

    def victory(self):
        print "Loser. I win - again. This is getting boring"
        exit()

    def defeat(self):
        print "You must've cheated... You damn cunt"
        exit()

    #printAll function (self explanatory) - STATUS:
    def printAll(self):
        print dir()
        print globals()
        print locals()

    #Function for finding out if the game has been won or lost - STATUS: SHOULD WORK, NOT TESTED
    def checkGameStatus(self):
        #global hit, losses
        if len(self.hit) > 16: #If 17 hits have been made
            self.victory()
        elif self.losses > 16:
            self.defeat()

    #Function that sees if the opponent has made a hit (ONLY TO BE CALLED WHEN THE OPPONENT HAS SENT COORDINATES)
    #Returns a string ("SUNK", "HIT" or "MISS")
    # STATUS: WORKS
    def areWeHit(self, response):
        #global ship1, ship2, ship3, ship4, ship5, losses

        miss = True

        if response == "printAll":
            self.printAll()
        elif response == "exit":
            print "Prf, looser"
            exit()
        # ELSEIF INPUT IS NOT COORDINATES

        #CHECKING IF SHIP1 HAS BEEN HIT!
        for i in self.ship1: #iterate through the coordinates of the first ship
            if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
                miss = False
                self.ship1.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
                self.losses = losses + 1

                if not self.ship1: #if ship1 is empty and all the coordinates have been shot
                    return "SUNK"
                    #DO SOMETHING MORE TO KEEP THE GAME AGOING
                else: #if the ship isn't sunk yet
                    return "HIT"
        #CHECKING IF SHIP2 HAS BEEN HIT!
        for i in self.ship2: #iterate through the coordinates of the first ship
            if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
                miss = False
                self.ship2.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
                self.losses = losses + 1

                if not ship2: #if ship1 is empty and all the coordinates have been shot
                    return "SUNK"
                    #DO SOMETHING MORE TO KEEP THE GAME AGOING
                else: #if the ship isn't sunk yet
                    return "HIT"
        #CHECKING IF SHIP3 HAS BEEN HIT!
        for i in self.ship3: #iterate through the coordinates of the first ship
            if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
                miss = False
                self.ship3.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
                self.losses = losses + 1

                if not ship3: #if ship1 is empty and all the coordinates have been shot
                    return "SUNK"
                    #DO SOMETHING MORE TO KEEP THE GAME AGOING
                else: #if the ship isn't sunk yet
                    return "HIT"
        #CHECKING IF SHIP4 HAS BEEN HIT!
        for i in self.ship4: #iterate through the coordinates of the first ship
            if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
                miss = False
                self.ship4.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
                self.losses = losses + 1

                if not ship4: #if ship1 is empty and all the coordinates have been shot
                    return "SUNK"
                    #DO SOMETHING MORE TO KEEP THE GAME AGOING
                else: #if the ship isn't sunk yet
                    return "HIT"
        #CHECKING IF SHIP5 HAS BEEN HIT!
        for i in self.ship5: #iterate through the coordinates of the first ship
            if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
                miss = False
                self.ship5.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
                self.losses = losses + 1

                if not ship5: #if ship1 is empty and all the coordinates have been shot
                    return "SUNK"
                    #DO SOMETHING MORE TO KEEP THE GAME AGOING
                else: #if the ship isn't sunk yet
                    return "HIT"
        if miss == True:
            return "MISS"
        elif self.losses == 15:
            print "GAME OVER!"
            exit()

    def testing(self):
        global currentTargetCoordinates, ship1, ship2, ship3, ship4, ship5

        print "Positioning ships! ..."
        positionShips()
        print ship1
        print ship2
        print ship3
        print ship4
        print ship5

        while (True):
            attack(codod)
            print currentTargetCoordinates
            opponentAnswer(raw_input("> "))
            print "codod = " + str(codod)

    def brain(self):
        global codod, currentTargetCoordinates
        print "send msg to server"
        server.sendmsg(server.channel,raw_input("> "))
        print "Okay, so you get to start, because my father was too lazy to finish me off ;)"
        while(True):
            print "Your turn!"
            print self.areWeHit(raw_input(">>> "))
            self.checkGameStatus()
            self.attack(self.codod)
            print self.currentTargetCoordinates
            self.opponentAnswer(raw_input(">>>"))
            self.checkGameStatus()

shit = supermegakillerbot()

shit.brain()