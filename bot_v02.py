__author__ = 'rohdehoved'
import ircClient as server
import time
from random import randint

class BattleBot:
    searchForDirection = 0 #integer used when a ship has been located. Check line underneath:
        # 0 means that we haven't searched any directions yet. 1 means we've shot to the right. 2 means we've tried both the right and the top.
        # 3 means we've tried botht the right, top and the left. 4 means we've shot at the bottom, and then all directions have been tried. Something is
        # wrong then.

    def brain(self):
        gameOver = False
        codod = 0
        missed = []
        hit = []
        currentShip = []

        while(gameOver == False):
            server.sendmsg(server.channel, "Welcome to Rohde's Battleship Bot. My game, my rules. I start!")
            server.sendmsg(server.channel, self.attack(codod, currentShip))
            server.sendmsg(server.channel, raw_input(">>>"))


    def attack(self, codod, currentShip):
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
            targetCoordinates = self.directShot()
            if self.checkIfPrevTarg(targetCoordinates):
                print "Something has gone terribly wrong, cheating suspected: directShot returns a coordinate that has already been shot at (ships are laying over each other)"

    def circleShot(self, currentShip):
        newCoordinates = currentShip[0] # stores the coordinates which have been succesfully shot, and is the first hit on the current ship

        if self.searchForDirection == 0: #if we just started searching for the rest of the ship, shoot to the right (increase x)
            newCoordinates[0] = newCoordinates[0] + 1 #increase x value (shoot to the right)
            self.searchForDirection = 1 # so the bot knows that it has shot to the right
        elif self.searchForDirection == 1: #if we already shot to the right in the search for the rest of the ship, shoot above (decrease y)
            newCoordinates[1] = newCoordinates[1] - 1
            self.searchForDirection = 2 #so the bot knows that it has shot above
        elif self.searchForDirection == 2: #if we already shot above in the search for the rest of the ship, shoot to the left (decrease x)
            newCoordinates[0] = newCoordinates[0] - 1
            self.searchForDirection = 3 #so the bot knows it has shot to the left
        elif self.searchForDirection == 3: #if we already shot to the left in the search for the rest of the ship, shoot below (increase y)
            newCoordinates[1] = newCoordinates[1] + 1
            self.searchForDirection = 4 #so the bot knows it has shot below

        return newCoordinates

    def checkIfPrevTarg(self, coordinates, missed, hit):
        for i in missed:
            if coordinates == i: #If the coordinates have already been targeted
               return True
        for i in hit:
            if coordinates == i: #If the coordinates have already been targeted
                return True
        return False

#test
ircclient = server.IrcClient()
serverlistener = server.serverListener(ircclient)
ircclient.start()
ircclient.sendmsg(server.channel, "hello")
obj = BattleBot()
obj.brain

