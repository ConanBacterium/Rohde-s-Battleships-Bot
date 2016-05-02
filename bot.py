__author__ = 'rohdehoved'
from random import randint

CODOD = 0
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

#positionShips function (self explanatory) - STATUS: WORKS
def positionShips():
    global ship1, ship2, ship3, ship4, ship5;
    ship1 = funnyStuff(5, randint(1,10)) #tells the funnyStuff that the ship1 has to be filled with 2 coordinations (that's the size of the ship)
    ship2 = funnyStuff(3, randint(1,10)) #Same shit
    ship3 = funnyStuff(3, randint(1,10)) #^ the randint is to randomize if the ship should be ver or hor, if divisible by 2 it's ver, else hor
    ship4 = funnyStuff(2, randint(1,10)) #^
    ship5 = funnyStuff(2, randint(1,10)) #^

#funnyStuff (I lacked the creativity to find a good name for this function) - STATUS: WORKS
def funnyStuff(sizeOfShip, verOrHor): #ver == divisible by 2, hor == undivisible by 2 #!!"#)!"#!"# RIGHT NOW IT DOESN'T USE THE VERORHOR!! !)"=#!"#)
    global allShipCoordinates
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
            if theCoordinate in allShipCoordinates: # If theCoordinate is already used
                legit = False # Makes sure that the coordinates won't be given to the alLShipCoordinations and that the coordinates list will be cleaned
            elif theCoordinate not in allShipCoordinates: #If theCoordinate is not in use
                coordinates.append(theCoordinate) #append theCoordinate

        if legit == True:
            for i in coordinates:
                allShipCoordinates.append(i) #Puts all the newly given coordinates into the allShipCoordinations
            break #Get out of the while loop, because none of the coordinates were in use
        elif legit == False:
            del coordinates[:] #clean the coordinates list
    return coordinates

#STATUS: WORKS
def attack(CODOD):
    if CODOD == 0:
        randomShot()
    elif CODOD == 1:
        circleShot()
    elif CODOD > 1:
        directShot()

#STATUS: WORKS
def opponentAnswer(response):
    global CODOD, currentShip, startPoints, searchForDirection, missed, hit, currentTargetCoordinates

    if response == "SUNK":
        hit.append(currentTargetCoordinates)
        CODOD = 1 # circle shoot
        if startPoints: #if startPoints is not empty
            startPoints.pop(0) #remove first element

        currentShip = [] #clear currentShip
        if startPoints:
            currentShip.append(startPoints[0]) #append the (new) first element of startPoints.

        searchForDirection = 0 # meaning we haven't found out the direction of the ship yet
        if not startPoints: # if startPoints is empty
            CODOD = 0 # no ship has been located, shoot random

    elif response == "MISS":
        missed.append(currentTargetCoordinates)
        if CODOD == 2:
            CODOD = 3
            # last element of currentShip has to be the same as the new one, because directShot function looks for the last element of currentShip and shoots with that as a reference point, and since we're shooting at the other end now, the reference point is the first place we shot at
            currentShip.append(currentShip[0])
        elif CODOD == 3: #if several ships laying beside each other has been reached
            CODOD = 1
            startPoints = currentShip
            currentShip = []
            currentShip.append(startPoints[0])

    elif response == "HIT":
        hit.append(currentTargetCoordinates)
        currentShip.append(currentTargetCoordinates)
        if CODOD == 1:
            CODOD = 2
        elif CODOD == 0:
            CODOD = 1


 # STATUS: WORKS

def randomShot():
    global currentTargetCoordinates
    currentTargetCoordinates = str(randint(1, 10)) + "," + str(randint(1,10)) #get random coordinates
    while checkIfPrevTarg(currentTargetCoordinates) == True: #as long as the coordinates have been shot at before, try with new coordinates
        currentTargetCoordinates = str(randint(1, 10)) + "," + str(randint(1,10)) #get random coordinates

#STATUS: WORKS - THOUGH YOU HAVE TO MAKE SURE THAT IT DOESN'T SHOOT FOR THE SAME PLACE TWICE
def circleShot():
     global currentTargetCoordinates, currentShip, searchForDirection
     a = currentShip[0].split(",") #currentShip should only contain ONE string/element, as we're supposed to locate the rest of the ship
     temp = [int(a[0]), int(a[1])] #casting from string to int

     if searchForDirection == 0: #if we just started searching for the rest of the ship, shoot to the right (increase x)
         temp[0] = temp[0] + 1 #increase x value (shoot to the right)
         searchForDirection = 1 # so the bot knows that it has shot to the right
     elif searchForDirection == 1: #if we already shot to the right in the search for the rest of the ship, shoot above (decrease y)
         temp[1] = temp[1] - 1
         searchForDirection = 2 #so the bot knows that it has shot above
     elif searchForDirection == 2: #if we already shot above in the search for the rest of the ship, shoot to the left (decrease x)
         temp[0] = temp[0] - 1
         searchForDirection = 3 #so the bot knows it has shot to the left
     elif searchForDirection == 3: #if we already shot to the left in the search for the rest of the ship, shoot below (increase y)
         temp[1] = temp[1] + 1
         searchForDirection = 4 #so the bot knows it has shot below

     currentTargetCoordinates = str(temp[0]) + "," + str(temp[1])#Put the new coordinates into the currentTargetCoordinates
     #if(checkIfPrevTarg(currentTargetCoordinates)):
      #   searchForDirection = searchForDirection + 1
       #  circleShot()

#STATUS: WORKS
def directShot():
    global searchForDirection, currentTargetCoordinates, CODOD
    if searchForDirection == 1: #if the ship lays horizontally and the bot started shooting to the right
        if CODOD == 3: #if end is reached shoot to the left of the first element
            a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[0] = temp[0] - 1 #decrease the x value (the first element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

        elif CODOD == 2: #shoot to the right
             a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
             temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
             temp[0] = temp[0] + 1 #increase the x value (the first element)

             currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

    elif searchForDirection == 2: #if the ship lays vertically, and the bot started shooting above
        if CODOD == 3: #if end is reached shoot below
            a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[1] = temp[1] + 1 #increase the y value (the second element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

        elif CODOD == 2: #shoot above the last element
            a = currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[1] = temp[1] - 1 #decrease the y value (the second element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

    elif searchForDirection == 3: #if the ship lays horizontally, and the bot started shooting to the left
        if CODOD == 3: #if end is reached shoot to the right of the first element
            a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[0] = temp[0] + 1 #decrease the x value (the second element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates


        elif CODOD == 2: #if end is not reached -  #shoot to the left of the last element
            a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[0] = temp[0] - 1 #decrease the x value (the second element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

    elif searchForDirection == 4: #if the ship lays vertically, and the bot started shooting below
        if CODOD == 3: #if end is reached shoot above the first element
            a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[1] = temp[1] - 1 #decrease the y value (the second element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

        elif CODOD == 2: #if end is not reached - #shoot below the last element
            a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
            temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
            temp[1] = temp[1] + 1 #decrease the y value (the second element)

            currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

#Function for checking if a coordinate has been targeted before - STATUS: WORKS
def checkIfPrevTarg(coordinates):
    global missed, hit
    prevTarg = False
    for i in missed:
        if coordinates == i: #If the coordinates have already been targeted
           return True
    for i in hit:
        if coordinates == i: #If the coordinates have already been targeted
            return True
    return False

def victory():
    print "Loser. I win - again. This is getting boring"
    exit()

def defeat():
    print "You must've cheated... You damn cunt"
    exit()

#printAll function (self explanatory) - STATUS:
def printAll():
    print dir()
    print globals()
    print locals()

#Function for finding out if the game has been won or lost - STATUS: SHOULD WORK, NOT TESTED
def checkGameStatus():
    global hit, losses
    if len(hit) > 16: #If 17 hits have been made
        victory()
    elif losses > 16:
        defeat()

#Function that sees if the opponent has made a hit (ONLY TO BE CALLED WHEN THE OPPONENT HAS SENT COORDINATES)
#Returns a string ("SUNK", "HIT" or "MISS")
# STATUS: WORKS
def areWeHit(response):
    global ship1, ship2, ship3, ship4, ship5, losses

    miss = True

    if response == "printAll":
        printAll()
    elif response == "exit":
        print "Prf, looser"
        exit()
    # ELSEIF INPUT IS NOT COORDINATES

    #CHECKING IF SHIP1 HAS BEEN HIT!
    for i in ship1: #iterate through the coordinates of the first ship
        if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
            miss = False
            ship1.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
            losses = losses + 1

            if not ship1: #if ship1 is empty and all the coordinates have been shot
                return "SUNK"
                #DO SOMETHING MORE TO KEEP THE GAME AGOING
            else: #if the ship isn't sunk yet
                return "HIT"
    #CHECKING IF SHIP2 HAS BEEN HIT!
    for i in ship2: #iterate through the coordinates of the first ship
        if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
            miss = False
            ship2.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
            losses = losses + 1

            if not ship2: #if ship1 is empty and all the coordinates have been shot
                return "SUNK"
                #DO SOMETHING MORE TO KEEP THE GAME AGOING
            else: #if the ship isn't sunk yet
                return "HIT"
    #CHECKING IF SHIP3 HAS BEEN HIT!
    for i in ship3: #iterate through the coordinates of the first ship
        if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
            miss = False
            ship3.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
            losses = losses + 1

            if not ship3: #if ship1 is empty and all the coordinates have been shot
                return "SUNK"
                #DO SOMETHING MORE TO KEEP THE GAME AGOING
            else: #if the ship isn't sunk yet
                return "HIT"
    #CHECKING IF SHIP4 HAS BEEN HIT!
    for i in ship4: #iterate through the coordinates of the first ship
        if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
            miss = False
            ship4.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
            losses = losses + 1

            if not ship4: #if ship1 is empty and all the coordinates have been shot
                return "SUNK"
                #DO SOMETHING MORE TO KEEP THE GAME AGOING
            else: #if the ship isn't sunk yet
                return "HIT"
    #CHECKING IF SHIP5 HAS BEEN HIT!
    for i in ship5: #iterate through the coordinates of the first ship
        if i == response: #if the coordinate is the one being shot at IF THE SHIP HAS BEEN SHOT
            miss = False
            ship5.remove(i) #removes the coordinate which has been shot at (used so we can later on check if the ship1 list is empty, which will mean that it has been sunk)
            losses = losses + 1

            if not ship5: #if ship1 is empty and all the coordinates have been shot
                return "SUNK"
                #DO SOMETHING MORE TO KEEP THE GAME AGOING
            else: #if the ship isn't sunk yet
                return "HIT"
    if miss == True:
        return "MISS"
    elif losses == 15:
        print "GAME OVER!"
        exit()

def testing():
    global currentTargetCoordinates, ship1, ship2, ship3, ship4, ship5

    print "Positioning ships! ..."
    positionShips()
    print ship1
    print ship2
    print ship3
    print ship4
    print ship5

    while (True):
        attack(CODOD)
        print currentTargetCoordinates
        opponentAnswer(raw_input("> "))
        print "CODOD = " + str(CODOD)

def brain():
    global CODOD, currentTargetCoordinates
    print "Okay, so you get to start, because my father was too lazy to finish me ;)"
    while(True):
        print "Your turn!"
        print areWeHit(raw_input(">>> "))
        checkGameStatus()
        attack(CODOD)
        print currentTargetCoordinates
        opponentAnswer(raw_input(">>>"))
        checkGameStatus()


brain()