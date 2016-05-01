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
     print "currentShip = " + str(currentShip)
     print "searchForDirection = " + str(searchForDirection)
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
    print "CODOD = " + str(CODOD)
    print "searchForDirection = " + str(searchForDirection)
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

# Attack:
# Step 1) startpoints is empty, so shoot random
# Step 2) startpoint is not empty, but currentShip is, so take first element of startpoint and put it into the currentShip. Now do the CODOD.
# Step 3) startpoint is not empty, neither is currentShip. Do the CODOD.

def testing():
    global currentTargetCoordinates, CODOD
    while (True):
        attack(CODOD)
        print currentTargetCoordinates
        opponentAnswer(raw_input("> "))
        print "CODOD = " + str(CODOD)

testing()