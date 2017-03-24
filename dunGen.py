# -*- coding: utf-8 -*-
import random
import math

class dunGen():
    
    def __init__(self, xDis, yDis, numRm, floorNum): #Dungon constructor
        self.x = xDis
        self.y = yDis
        self.pStartX = 0
        self.pStartY = 0
        self.f = floorNum
        self.r = numRm
        self.D = [[tile(True, False) for i in range(self.y + 1)] for i in range(self.x + 1)]
        self.Rooms = []
    
    def genDun(self):
        #self.genWalls()
        self.genRooms(room(1, self.x - 1, 1, self.y - 1,))
        self.genHalls()
        self.genLadder()
        
    def printDn(self, objs): #Prints the dungeon
        for y in range(self.y + 1):
            temp = ""
            for x in range(self.x + 1):
                self.D[x][y].update()
                objPrint = False
                for i in range(len(objs)):
                    if(objs[i].x == x and objs[i].y == y):
                        temp = temp + str(objs[i].i)
                        objPrint = True
                if(objPrint == False):
                	temp = temp + str(self.D[x][y].i)
            print(temp)
    
    def printDnNoObjs(self): #Prints the dungeon without objects (just the walls)
        for y in range(self.y + 1):
            temp = ""
            for x in range(self.x + 1):
                self.D[x][y].update()
                temp += self.D[x][y].i
            print(temp)
    
    def genWalls(self): #Generates the ring of outer walls of the dungeon
        for y in range(self.y + 1):
            for x in range(self.x + 1):
                if((y == 0 or y == self.y - 1) or (x == 0 or x == self.x - 1)):
                    self.D[x][y].update()
                    self.D[x][y].s = True
    
    def genRooms(self, r): #Generates the rooms in the dungeon-- revised!
        if(r.xRange > 3 and r.yRange > 3):
            c = random.randint(0, 1)
            if(c == 0): #Splits the room horizontally
                y = random.randint(r.yMin + 2, r.yMax - 2)
                while(y == self.pStartY):
                    y = random.randint(r.yMin + 2, r.yMax - 2)
                self.genRooms(room(r.xMin, r.xMax, r.yMin, y - 1))
                self.genRooms(room(r.xMin, r.xMax, y + 1, r.yMax))
            if(c == 1): #Splits the room vertically
                x = random.randint(r.xMin + 2, r.xMax - 2)
                while(x == self.pStartX):
                    x = random.randint(r.xMin + 2, r.xMax - 2)
                self.genRooms(room(r.xMin, x - 1, r.yMin, r.yMax))
                self.genRooms(room(x + 1, r.xMax, r.yMin, r.yMax))
        elif(r.xRange > 5): #Splits the room vertically
            x = random.randint(r.xMin + 2, r.xMax - 2)
            while(x == self.pStartX):
                    x = random.randint(r.xMin + 2, r.xMax - 2)
            self.genRooms(room(r.xMin, x - 1, r.yMin, r.yMax))
            self.genRooms(room(x + 1, r.xMax, r.yMin, r.yMax))
        elif(r.yRange > 5): #Splits the room horizontally
            y = random.randint(r.yMin + 2, r.yMax - 2)
            while(y == self.pStartY):
                    y = random.randint(r.yMin + 2, r.yMax - 2)
            self.genRooms(room(r.xMin, r.xMax, r.yMin, y - 1))
            self.genRooms(room(r.xMin, r.xMax, y + 1, r.yMax))
        else:
            for y in range(r.yMin, r.yMax + 1):
                for x in range(r.xMin, r.xMax + 1):
                    self.D[x][y].s = False
            self.Rooms.append(r)
    
    def genHalls(self):
        for i in range(len(self.Rooms)): #Creates a neighborhood get-together for all of the rooms!
            self.findNeighbors(self.Rooms[i])
        pos = random.randint(0, len(self.Rooms) - 1)
        r = self.Rooms[pos]
        nPos = random.randint(0, len(r.neighbors) - 1)
        r2 = r.neighbors[nPos]
        allPicked = False
        while(self.checkForErrors() and allPicked == False):
            allPicked = True
            for i in range(len(self.Rooms)):
                if(self.Rooms[i].picked == False):
                    allPicked = False
            #if(allPicked == False):
            #    print("allPicked == False")
            if(0 <= pos <= len(self.Rooms) - 1):
                r = self.Rooms[pos]
            nPos = random.randint(0, len(r.neighbors) - 1)
            r2 = r.neighbors[nPos]
            while(r2.picked and allPicked == False):
                allPicked = True
                for i in range(len(self.Rooms)):
                    if(self.Rooms[i].picked == False):
                        allPicked = False
                #print("r2 picked, pos = " + str(pos) + ", nPos = " + str(nPos) + ", len = " + str(len(r.neighbors)))
                for i in range(0, len(r.neighbors)):
                    nPos += 1
                    if(nPos >= len(r.neighbors)):
                        nPos = 0
                    if(r2.picked):
                        r2 = r.neighbors[nPos]
                if(r2.picked):
                    pos += 1
                    if(pos >= len(self.Rooms)):
                        pos = 0
                    r = self.Rooms[pos]
                    nPos = random.randint(0, len(r.neighbors) - 1)
                    r2 = r.neighbors[nPos]
            else:
                #print("r2 not picked, pos = " + str(pos) + ", nPos = " + str(nPos))
                if(r.yMin > r2.yMax):
                    #print("Up"),
                    for x in range(r.xMin, r.xMax + 1): #Up
                        if(self.findRoom(x, r.yMin - 2) == r2):
                            self.D[x][r.yMin - 1].s = False
                            self.D[x][r.yMin - 1].nImg = ".."
                            r.picked = True
                            r2.picked = True
                            pos = self.Rooms.index(r2)
                if(r.yMax < r2.yMin):
                    #print("Down"),
                    for x in range(r.xMin, r.xMax + 1): #Down
                        if(self.findRoom(x, r.yMax + 2) == r2):
                            self.D[x][r.yMax + 1].s = False
                            self.D[x][r.yMax + 1].nImg = ".."
                            r.picked = True
                            r2.picked = True
                            pos = self.Rooms.index(r2)
                if(r.xMin > r2.xMax):
                    #print("Left"),
                    for y in range(r.yMin, r.yMax + 1): #Left
                        if(self.findRoom(r.xMin - 2, y) == r2):
                            self.D[r.xMin - 1][y].s = False
                            self.D[r.xMin - 1][y].nImg = ".."
                            r.picked = True
                            r2.picked = True
                            pos = self.Rooms.index(r2)
                if(r.xMax < r2.xMin):
                    #print("Right"),
                    for y in range(r.yMin, r.yMax + 1): #Right
                        if(self.findRoom(r.xMax + 2, y) == r2):
                            self.D[r.xMax + 1][y].s = False
                            self.D[r.xMax + 1][y].nImg = ".."
                            r.picked = True
                            r2.picked = True
                            pos = self.Rooms.index(r2)
                #print("Run")
                #print
    
    def genLadder(self):
        minNeighbors = 1
        done = False
        while(done == False):
            for i in range(len(self.Rooms)):
                if(len(self.Rooms[i].neighbors) <= minNeighbors and distance(self.pStartX, self.pStartY, (self.Rooms[i].xMin + self.Rooms[i].xMax) / 2, (self.Rooms[i].yMin + self.Rooms[i].yMax) / 2) >= self.x / 2 and done == False):
                    self.D[(self.Rooms[i].xMin + self.Rooms[i].xMax) / 2][(self.Rooms[i].yMin + self.Rooms[i].yMax) / 2].h = True
                    done = True
            minNeighbors += 1
    
    def findNeighbors(self, r): #Tells a room what it's neighbors are-- so it can make a happy neighborhood :)
        for x in range(r.xMin, r.xMax): #Checks for neighbors upwards
            rTemp = self.findRoom(x, r.yMin - 2)
            if(rTemp != None and (not rTemp in r.neighbors)):
                r.neighbors.append(rTemp)
        for y in range(r.yMin, r.yMax): #Checks for neighbors to the left
            rTemp = self.findRoom(r.xMin - 2, y)
            if(rTemp != None and (not rTemp in r.neighbors)):
                r.neighbors.append(rTemp)
        for x in range(r.xMin, r.xMax): #Checks for neighbors downwards
            rTemp = self.findRoom(x, r.yMax + 2)
            if(rTemp != None and (not rTemp in r.neighbors)):
                r.neighbors.append(rTemp)
        for y in range(r.yMin, r.yMax): #Checks for neighbors to the right
            rTemp = self.findRoom(r.xMax + 2, y)
            if(rTemp != None and (not rTemp in r.neighbors)):
                r.neighbors.append(rTemp)
    
    def findRoom(self, x, y):
        for i in range(len(self.Rooms)):
            if(self.Rooms[i].xMin <= x <= self.Rooms[i].xMax and self.Rooms[i].yMin <= y <= self.Rooms[i].yMax):
                return self.Rooms[i]
        return
    
    def check(self, x, y): #Makes sure that the dungeon has no unconnected rooms.          
        if(self.inRange(x + 1, y) and self.D[x + 1][y].s == False and self.D[x + 1][y].c == False): #Right
            self.D[x + 1][y].i = "##"
            self.D[x + 1][y].c = True
            self.check(x + 1, y)
        if(self.inRange(x - 1, y) and self.D[x - 1][y].s == False and self.D[x - 1][y].c == False): #Left
            self.D[x - 1][y].i = "##"
            self.D[x - 1][y].c = True
            self.check(x - 1, y)
        if(self.inRange(x, y - 1) and self.D[x][y - 1].s == False and self.D[x][y - 1].c == False): #Up
            self.D[x][y - 1].i = "##"
            self.D[x][y - 1].c = True
            self.check(x, y - 1)
        if(self.inRange(x, y + 1) and self.D[x][y + 1].s == False and self.D[x][y + 1].c == False): #Down
            self.D[x][y + 1].i = "##"
            self.D[x][y + 1].c = True
            self.check(x, y + 1)
    
    def unCheck(self): #Undoes check, so the dungeon can be checked again
        for y in range(self.y):
            for x in range(self.x):
                if(self.D[x][y].c == True):
                    self.D[x][y].update()
                    self.D[x][y].c = False

    def inRange(self, x, y): #Makes sure that the coordinate is inside the dungeon's range.
        if(x >= 0 and x < self.x and y >= 0 and y < self.y):
            return True
        return False
    
    def checkRow(self, y): #Checks the row at (y) ...what else did you think this one did?
        unChecked = False
        for i in range(self.x):
            if(self.D[i][y].s == False and self.D[i][y].c == False):
                unChecked = True
        return unChecked
    
    def checkCol(self, x): #Checks the column at (x) ...still just a checking method...
        unChecked = False
        for i in range(self.y):
            if(self.D[x][i].s == False and self.D[x][i].c == False):
                unChecked = True
        return unChecked     
    
    def checkForErrors(self): #Used to make sure that there are no unconnected rooms.
        self.unCheck()
        self.check(self.pStartX, self.pStartY)
        error = False
        for y in range(self.y):
            for x in range(self.x):
                if(self.D[x][y].s == False and self.D[x][y].c == False and error == False):
                    error = True
        self.unCheck()
        return error
            
    def sTile(self, x, y, img): #Sets the tile at the given coordinates.
        self.D[x][y].i = img
    
    def gTile(self, x, y): #Gets the tile at the given coordinates.
        return self.D[x][y]
        
class tile():
    
    def __init__(self, solid, checked):
        self.i = "  "
        self.s = solid
        self.c = checked
        self.l = False
        self.h = False
        self.tOptions = ["[]"]
        self.fOptions = ["  "]
        self.sImg = random.choice(self.tOptions)
        self.nImg = random.choice(self.fOptions)
        self.update()
    
    def update(self):
        if(self.s == True):
            self.i = self.sImg
        elif(self.s == False):
            if(self.h == True):
                self.i = "<>"
            elif(self.l == True):
                self.i = "||"
            else:
                self.i = self.nImg

class player():
    
    def __init__(self, img):
        self.x = 0
        self.y = 0
        self.i = img
        self.D = []
        
    def move(self, xPos, yPos):
        if(self.D.gTile(self.x + xPos, self.y + yPos).s == False):
            self.x = self.x + xPos
            self.y = self.y + yPos

class room():
    
    def __init__(self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.xRange = xMax - xMin
        self.yMin = yMin
        self.yMax = yMax
        self.yRange = yMax - yMin
        self.neighbors = []
        self.picked = False

#Other Methods#
def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def init(p, d, dX, dY):
    d.append(dunGen(dX, dY, random.randint(dX / 3, dX / 2), 0))
    p.D = d[0]
    p.x = d[0].x / 2
    p.y = d[0].y / 2
    d[0].pStartX = p.x
    d[0].pStartY = p.y
    d[0].genDun()
    
#Main#

#
dunPos = 0
dX = 35
dY = 35
#

p1 = player("@" + random.choice(['/', ']', ')', '|', '!']))
Dun = []
init(p1, Dun, dX, dY)

objs = [p1]
usr = ""

Dun[0].printDn(objs)
"""
while(usr != "q"): #Main Loop
    Dun[dunPos].printDn(objs)
    usr = raw_input("> ")
    usr = str(usr)
    if(usr.lower() == "w"):
        p1.move(0,-1)
    if(usr.lower() == "a"):
        p1.move(-1,0)
    if(usr.lower() == "s"):
        p1.move(0, 1)
    if(usr.lower() == "d"):
        p1.move(1, 0)
    if(usr.lower() == "down" and Dun[dunPos].D[p1.x][p1.y].h == True):
        dunPos += 1
        if(dunPos >= len(Dun)):
            Dun.append(dunGen(dX, dY, random.randint(dX / 3, dX / 2), 0))
            p1.D = Dun[dunPos]
            Dun[dunPos].pStartX = p1.x
            Dun[dunPos].pStartY = p1.y
            print("(" + str(Dun[dunPos].pStartX) + ", " + str(Dun[dunPos].pStartY) + ")")
            Dun[dunPos].genDun()
            print(Dun[dunPos].checkForErrors())
            Dun[dunPos].D[p1.x][p1.y].l = True
        print("You decend to floor " + str(dunPos) + ".")
    if(usr.lower() == "up" and Dun[dunPos].D[p1.x][p1.y].l == True):
        dunPos -= 1
        print("You ascend to floor " + str(dunPos) + ".")
"""