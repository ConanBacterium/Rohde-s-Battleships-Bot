__author__ = 'rohdehoved'
from random import randint

allShipCoordinations = []
missed = [] #list with coordinates of shots that missed (strings)
hit = [] #list with coordinates of shots that hit (strings)
currentTargetCoordinates = ""
losses = 0 #amount of losses/hits on own ships
currentShip = [] #list with coordinates of the ship that is being attacked atm (empty if searching for ship)
endReached = False # boolean for whether or not an end of the ship currently being attacked has been reached, if it has, shoot at the other end
ship1 = [] # 5 blocks
ship2 = [] # 3 blocks
ship3 = [] # 3 blocks
ship4 = [] # 2 blocks
ship5 = [] # 2 blocks
searchForDirection = 0 #integer used when a ship has been located. Check line underneath:
# 0 means that we haven't searched any directions yet. 1 means we've shot to the right. 2 means we've tried both the right and the top.
# 3 means we've tried botht the right, top and the left. 4 means we've shot at the bottom, and then all directions have been tried. Something is
# wrong then.
iLackedTheCreativityToGiveThisVariableAProperName = False #variable used to find out if the bot has shot one time after the end has been reached.
#this is to know whether too shoot from the first element in the currentShip[] or from the last element :)


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
    global allShipCoordinations
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
            if theCoordinate in allShipCoordinations: # If theCoordinate is already used
                legit = False # Makes sure that the coordinates won't be given to the alLShipCoordinations and that the coordinates list will be cleaned
            elif theCoordinate not in allShipCoordinations: #If theCoordinate is not in use
                coordinates.append(theCoordinate) #append theCoordinate

        if legit == True:
            for i in coordinates:
                allShipCoordinations.append(i) #Puts all the newly given coordinates into the allShipCoordinations
            break #Get out of the while loop, because none of the coordinates were in use
        elif legit == False:
            del coordinates[:] #clean the coordinates list
    return coordinates

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

#Function for shooting at a  random coordinate - STATUS: WORKS
def shootRandom():
    global currentTargetCoordinates
    currentTargetCoordinates = str(randint(1, 10)) + "," + str(randint(1,10)) #get random coordinates
    while checkIfPrevTarg(currentTargetCoordinates) == True: #as long as the coordinates have been shot at before, try with new coordinates
        currentTargetCoordinates = str(randint(1, 10)) + "," + str(randint(1,10)) #get random coordinates

#Function for finding out if the game has been won or lost - STATUS: SHOULD WORK, NOT TESTED
def checkGameStatus():
    global missed, hit, losses, ship1, ship2, ship3, ship4, ship5, allShipCoordinations, currentShip, currentTargetCoordinates, endReached, myTurn
    global gameOver
    if hit.length > 16: #If 17 hits have been made
        victory()
    elif losses > 16:
        gameOver = True
        defeat()

#Function for clearing the currentShip list - STATUS: NOT TESTED, CAN'T NOT-WORK
def clearCurrentShip():
    global currentShip
    del currentShip[:]

#Function for putting opponents respond into list of missed or hit coordinations (MAY ONLY BE CALLED WHEN THE OPPONENT HAS RESPONDED WITH "MISS", "HIT" or "SUNK")
#STATUS: LOOKS LIKE IT WORKS
def updateLists(response): #ONLY TO BE USED
    global missed, hit, endReached, searchForDirection, iLackedTheCreativityToGiveThisVariableAProperName, currentShip
    if response == "MISS":
        missed.append(currentTargetCoordinates) #save the coordinates as misses
        if len(currentShip) > 1: #If a ship had been attacked more than once, the end has been reached. If it had only been attacked once,
                                 #we aren't sure if we've reached the end, we might just shoot in the wrong direction :)
            endReached = True #Tell that the end has been reached
            currentShip.append(currentShip[0]) #append the first coordinates to the end of the currentShip list.
    elif response == "HIT":
        hit.append(currentTargetCoordinates) #save the coordinates as hits
        currentShip.append(currentTargetCoordinates) #save the coordinates in the currentShip
    elif response == "SUNK":
        hit.append(currentTargetCoordinates) #save the coordinates as hits
        clearCurrentShip() #Tell the bot to try to find a new ship
        searchForDirection = 0 #Tell the bot to search for the rest of ship from the start, the next time it has a ship located
        endReached = False #the end has no longer been reached, as we are starting anew with finding and shooting at a ship
        iLackedTheCreativityToGiveThisVariableAProperName = False

    if len(hit) == 15:
        print "I WON! BYE"
        exit()
    # checkGameStatus() #check the game status, have we won (OUTCOMMENT WHEN FINISHED!!!)

#Function that sees if the opponent has made a hit (ONLY TO BE CALLED WHEN THE OPPONENT HAS SENT COORDINATES
#Returns a string ("SUNK", "HIT" or "MISS")
# STATUS: WORKS
def areWeHit(response):
    global ship1, ship2, ship3, ship4, ship5, losses

    miss = True

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

#locateRestOfShip function, used in attack if the ship we're attacking has only been hit once
#Status: FUCKING WORKS!!!
def locateRestOfShip():
    global currentTargetCoordinates, currentShip, searchForDirection
    a = currentShip[0].split(",") #currentShip should only contain ONE string/element, as we're supposed to locate the rest of the ship
    temp = [int(a[0]), int(a[1])]

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

#attack function
#IMPORTANT! In the if endReached == true, it says that it has to shoot below/above/left/right of the first element, but
# in updateLists the first element has been made the last element, so don't worry about that - just go for the last element :)
#return: attack coordinates
#Status: WORKS - I think... Check it again more neatly.
def attack():
    global currentShip, searchForDirection, currentTargetCoordinates
    if not currentShip: #if a ship hasn't been located
        shootRandom()
    elif len(currentShip) == 1: #if a ship has been located and only been hit once
        locateRestOfShip()
    elif len(currentShip) > 1: #if a ship has been located and hit more than once (so we've found out if it's vertical or horizontal on the grid)
        if searchForDirection == 1: #if the ship lays horizontally and the bot started shooting to the right
            if endReached: #if end is reached shoot to the left of the first element
                a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] - 1 #decrease the x value (the first element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

            elif not endReached: #shoot to the right
                a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] + 1 #increase the x value (the first element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

        elif searchForDirection == 2: #if the ship lays vertically, and the bot started shooting above
            if endReached: #if end is reached shoot below
                a = currentShip[-1].split(",") #last hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] + 1 #increase the y value (the second element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

            elif not endReached: #shoot above the last element
                a = currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] - 1 #decrease the y value (the second element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

        elif searchForDirection == 3: #if the ship lays horizontally, and the bot started shooting to the left
            if endReached: #if end is reached shoot to the right of the first element
                a = currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] + 1 #decrease the x value (the second element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates


            elif not endReached: #if end is not reached -  #shoot to the left of the last element
                a = currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[0] = temp[0] - 1 #decrease the x value (the second element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates

        elif searchForDirection == 4: #if the ship lays vertically, and the bot started shooting below
            if endReached: #if end is reached shoot above the first element
                a = currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] - 1 #decrease the y value (the second element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

            elif not endReached: #if end is not reached - #shoot below the last element
                a = currentShip[-1].split(",") #first hit on target coordinates made into a list of x and y
                temp = [int(a[0]), int(a[1])] #the exact same as a, it's just converted to integers so we can fuck around with it
                temp[1] = temp[1] + 1 #decrease the y value (the second element)

                currentTargetCoordinates = str(temp[0]) + "," + str(temp[1]) #Put the new coordinates into the currentTargetCoordinates as a string

    return currentTargetCoordinates

def brain():
    positionShips()
    print "I start!"
    while True:
        print attack()
        updateLists(raw_input())
        print areWeHit(raw_input("Your turn: "))




#test the attack function
def testAttack():
    global currentTargetCoordinates, currentShip
    while 1:
        print attack()
        updateLists(raw_input(">"))



def test():
    positionShips()
    print ship1
    print ship2
    print ship3
    print ship4
    print ship5

brain()

#TO DO LIST: MAKE A FUCKING FUNCTION THAT PRINTS OUT ALL VARIABLES

# hvis et skib har ramt koordinat-J og misser, men saa rammer et koordinat ved siden af, vil den alligevel proeve at ramme J...
# if the enemy places it's ships besides eachother, the bot won't know what to do. If the bot has hit something more than once, and then misses at both ends
#without sinking something, it has encountered two or more ships that lay beside each other.
#5,6
# >HIT
# 6,6
# >MISS
# 5,5
# >MISS
# 4,6
# >HIT
# 3,6
# >MISS
# 6,6
# >MISS
# 6,6
# >MISS
# 6,6
# >MISS
# 6,6
# >

# 3.4, 3.5, 3.6, 3.7