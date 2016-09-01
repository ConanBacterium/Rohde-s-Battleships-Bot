__author__ = 'rohdehoved'
import ircClient as server
import time
from random import randint
from collections import namedtuple

''' renaming that has to be done with the program is finished:
    codod = attackmode
    opponentanswer = updateModesAndLists #or something like that, something more descriptive

    When
'''

class BattleBot:
    searchForDirection = 0 #integer used when a ship has been located. Check line underneath:
        # 0 means that we haven't searched any directions yet. 1 means we've shot to the right. 2 means we've tried both the right and the top.
        # 3 means we've tried botht the right, top and the left. 4 means we've shot at the bottom, and then all directions have been tried. Something is
        # wrong then.

    missed = []
    hit = []
    startPoints = [] #holds all the coordinates of starting points of ships that we know of and haven't yet sinked/sunk
    codod = 0
    currentShip = [] # holds all the coordinates of the ship that we're attacking

    def __init__(self):
        self.ircclient = server.IrcClient()
        print "IrcClient object initiated"


        time.sleep(15) #wait 15 seconds for the connection to be established
        # !!!!    TEST    !!!!
        self.brain()

    def brain(self):
        print "BattleBot.brain()"
        gameOver = False
        currentTargetCoordinates = (0,0)

        self.sendmsg("Welcome to Rohde's Battleship Bot. My game, my rules - I start!")

        while(gameOver == False):
            print "Current state: " + str(self.codod)

            currentTargetCoordinates = self.getTargetCoordinates(self.codod, self.currentShip)
            print "got target coordinates"
            self.sendcoordinates(currentTargetCoordinates)
            print "sent target coordinates"
            self.opponentAnswer(self.recvanswer(), currentTargetCoordinates)#receive answer and update shizniz
            print "codod: " + str(self.codod)
            print "startPoints: " + str(self.startPoints)
            print "currentShip: " + str(self.currentShip)
            print"ran opponentAnswer()"
            self.recvcoordinate()
            print "received coordinate"
            #receive coordinates and respond with HIT/MISS/SUNK. Then shoot.

    def opponentAnswer(self, response, currentTargetCoordinates):

        print "opponentAnswer() function"
        print "response = " + response

        if "SUNK" in response:
            self.hit.append(currentTargetCoordinates)
            self.codod = 1 # circle shoot
            if self.startPoints: #if startPoints is not empty
                self.startPoints.pop(0) #remove first element

            self.currentShip = [] #clear currentShip # THIS FUCKING LINE IS BAD !?)?"!#= !"#!&/"()#/!"?(#/"! #
            if self.startPoints:
                self.currentShip.append(self.startPoints[0]) #append the (new) first element of startPoints.

            searchForDirection = 0 # meaning we haven't found out the direction of the ship yet
            if not self.startPoints: # if startPoints is empty
                self.codod = 0 # no ship has been located, shoot random
            print "opponentAnswer() response was SUNK"

        elif "MISS" in response:
            self.missed.append(currentTargetCoordinates)
            if self.codod == 2: ## if there has been shot to the right
                self.codod = 3 # set attack-mode to shoot to the left
                # last element of currentShip has to be the same as the new one, because directShot function looks for the last element of currentShip and shoots with that as a reference point, and since we're shooting at the other end now, the reference point is the first place we shot at
                self.currentShip.append(self.currentShip[0])
                self.currentShip.pop(0) #remove the first element to avoid duplicates. The currentShip is copied to startPoints, and if we then have duplicates we'll shoot at the same points.
            elif self.codod == 3: #if several ships laying beside each other has been reached (codod only reaches 3, when codod has already been 2 - which then means that there's been shot to the left and right.
                self.codod = 1
                self.startPoints = self.currentShip
                self.currentShip = [] # clear currentShip
                self.currentShip.append(self.startPoints[0])
            print "opponentAnswer() response was MISS"

        elif "HIT" in response:
            self.hit.append(currentTargetCoordinates)
            self.currentShip.append(currentTargetCoordinates)
            if self.codod == 1:
                self.codod = 2
            elif self.codod == 0:
                self.codod = 1
            print "opponentAnswer() response was HIT"

    def extractPrivMsg(self, msg):
        print "extractPrivmsg"
        nick = msg.split ( '!' ) [ 0 ].replace ( ':', '' )
        message = ':'.join ( msg.split ( ':' ) [ 2: ] )
        print nick + ':', message
        return msg


    def sendmsg(self, msg):
        self.ircclient.sendmsg(self.ircclient.channel, "battleshipmsg:" + msg)

    def recvcoordinate(self):
        msg = self.ircclient.recvbattleshipmsg()
        msg = self.extractPrivMsg(msg)
        print msg
        self.ircclient.ping(msg)
        while("," not in msg):
            msg = self.ircclient.s.recv(2048)
        print "RECEIVED A COORDINATE: " + msg
        # extract the coordinate from the irc message
        #return msg

    def recvanswer(self):
        msg = self.ircclient.recvbattleshipmsg()
        print "recvanswer() function received a msg from the server"
        msg = self.extractPrivMsg(msg)
        print "recvanswer() function ran extractPrivMsg"
        return msg

    def sendcoordinates(self, cds):
        msg = str(cds[0]) + "," + str(cds[1])
        self.sendmsg(msg)

    def getTargetCoordinates(self, codod, currentShip):
        targetCoordinates = ()

        if codod == 0:
            targetCoordinates = (randint(1, 10), randint(1,10))

            while(self.checkIfPrevTarg(targetCoordinates) == True): #make sure not too shoot at the same coordinate twice
                targetCoordinates = (randint(1,10), randint(1,10))

        elif codod == 1:
            targetCoordinates = self.circleShot(currentShip)

            while(self.checkIfPrevTarg(targetCoordinates) == True): #make sure not too shoot at the same coordinate twice
                targetCoordinates = self.circleShot(currentShip)
        elif codod > 1:
            targetCoordinates = self.directShot(codod, self.searchForDirection)
            if self.checkIfPrevTarg(targetCoordinates):
                print "Something has gone terribly wrong, cheating suspected: directShot returns a coordinate that has already been shot at (ships are laying over each other)"

        return targetCoordinates

    def circleShot(self, currentShip):
        newCoordinates = currentShip[0] # stores the coordinates which have been succesfully shot, and is the first hit on the current ship
        x = newCoordinates[0]
        y = newCoordinates[1]
        if self.searchForDirection == 0: #if we just started searching for the rest of the ship, shoot to the right (increase x)
            x = newCoordinates[0] + 1 #increase x value (shoot to the right)
            self.searchForDirection = 1 # so the bot knows that it has shot to the right
        elif self.searchForDirection == 1: #if we already shot to the right in the search for the rest of the ship, shoot above (decrease y)
            y = newCoordinates[1] - 1
            self.searchForDirection = 2 #so the bot knows that it has shot above
        elif self.searchForDirection == 2: #if we already shot above in the search for the rest of the ship, shoot to the left (decrease x)
            x = newCoordinates[0] - 1
            self.searchForDirection = 3 #so the bot knows it has shot to the left
        elif self.searchForDirection == 3: #if we already shot to the left in the search for the rest of the ship, shoot below (increase y)
            y = newCoordinates[1] + 1
            self.searchForDirection = 4 #so the bot knows it has shot below

        newCoordinates = (x, y)
        return newCoordinates

    def directShot(self, codod, searchForDirection):
        '''
            !!!HARDCODED!!!
        '''

        lastx = self.currentShip[-1][0] # x coordinate of the last hit on the currentShip.
        lasty = self.currentShip[-1][1] # y coordinate of the last hit on the currentShip.

        targetCoordinates = ()
        print "codod = " + str(codod)
        print "searchForDirection = " + str(searchForDirection)

        if searchForDirection == 1: #if the ship lays horizontally and the bot started shooting to the right
            if codod == 3: #if end is reached shoot to the left of the first element
                lastx = lastx - 1 #decrease the x value (the first element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

            elif codod == 2: #shoot to the right
                 lastx = lastx + 1 #increase the x value (the first element)

                 targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

        elif searchForDirection == 2: #if the ship lays vertically, and the bot started shooting above
            if codod == 3: #if end is reached shoot below
                lasty = lasty + 1 #increase the y value (the second element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

            elif codod == 2: #shoot above the last element
                lasty = lasty - 1 #decrease the y value (the second element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

        elif searchForDirection == 3: #if the ship lays horizontally, and the bot started shooting to the left
            if codod == 3: #if end is reached shoot to the right of the first element
                lastx = lastx + 1 #increase the x value (the second element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates


            elif codod == 2: #if end is not reached -  #shoot to the left of the last element
                lastx = lastx - 1 #decrease the x value (the second element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

        elif searchForDirection == 4: #if the ship lays vertically, and the bot started shooting below
            if codod == 3: #if end is reached shoot above the first element
                lasty = lasty - 1 #decrease the y value (the second element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

            elif codod == 2: #if end is not reached - #shoot below the last element
                lasty = lasty + 1 #decrease the y value (the second element)

                targetCoordinates = (lastx, lasty) #Put the new coordinates into the targetCoordinates

        return targetCoordinates

    def checkIfPrevTarg(self, coordinates):
        for i in self.missed:
            if coordinates == i: #If the coordinates have already been targeted
               return True
        for i in self.hit:
            if coordinates == i: #If the coordinates have already been targeted
                return True
        return False


bb = BattleBot()