import sys
import time
import os
from Astar import astar
from Qlearning import *

from enum import Enum
class Directions(Enum):
    UP = "up"
    RIGHT = "right"
    LEFT = "left"
    DOWN = "down"

    def __eq__(self, other):
        #if self.__class__ is other.__class__:
        #    return self.value == other.value
        #return NotImplemented
        return self.value == other.value

WALL = 'x'
EMPTY = '.'
PLAYER = 'p'

def readMaze(filename):
    lines = [line.rstrip('\n') for line in open(filename)]

    a = []
    for line in lines:
        a.append([ch for ch in line])

    return a

def printMaze(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(a[i][j], end="")
        print()


start = tuple()
finish = tuple()

def findStartAndFinish(a):
    global start
    global finish

    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] == 's':
                start = (i, j)
            elif a[i][j] == 'f':
                finish = (i, j)


def createWorkingMatrix(maze, startPos, nl, nc, dir):
    a = []
    if dir == Directions.UP:

        lMin = startPos[0]
        lMax = max(startPos[0] - nl, -1)
        
        cMin = max(startPos[1] - int(nc/2), 0);
        cMax = min(startPos[1] + int(nc/2) + 1, len(maze[0]))

        for i in range(lMin, lMax, -1):
            l = []
            for j in range(cMin, cMax):
                l.append(maze[i][j])
            a.append(l)
        
           
        #for i in range(nl):
        #    a.append(maze[startPos[0] - i][startPos[1] - int(nc/2) : startPos[1] + int(nc/2) + 1])
        #a[0][int(nc/2)] = PLAYER

    elif dir == Directions.DOWN:

        lMin = startPos[0]
        lMax = min(startPos[0] + nl, len(maze))

        cMin = max(startPos[1] - int(nc/2), 0);
        cMax = min(startPos[1] + int(nc/2) + 1, len(maze[0]))

        for i in range(lMin, lMax):
            l = []
            for j in range(cMin, cMax):
                l.append(maze[i][j])
            a.append(l)

        #for i in range(nl):
        #    a.append(maze[startPos[0] + i][startPos[1] - int(nc/2) : startPos[1] + int(nc/2) + 1])
        #a[0][int(nc/2)] = PLAYER
        
    elif dir == Directions.RIGHT:

        lMin = max(startPos[0] - int(nc/2), 0);
        lMax = min(startPos[0] + int(nc/2) + 1, len(maze))

        cMin = startPos[1]
        cMax = min(startPos[1] + nl, len(maze[0]))

        for i in range(lMin, lMax):
            l = []
            for j in range(cMin, cMax):
                l.append(maze[i][j])
            a.append(l)

        #for i in range(startPos[0] - int(nc/2), startPos[0] + int(nc/2) + 1):
        #    a.append(maze[i][startPos[1] : startPos[1] + nl])
        #a[int(nc/2)][0] = PLAYER

        # rotate 90
        a = list(zip(*a[::-1]))

    elif dir == Directions.LEFT:

        lMin = max(startPos[0] - int(nc/2), 0);
        lMax = min(startPos[0] + int(nc/2) + 1, len(maze))

        cMin = max(startPos[1] - nl + 1, 0);
        cMax = startPos[1] + 1

        for i in range(lMin, lMax):
            l = []
            for j in range(cMin, cMax):
                l.append(maze[i][j])
            a.append(l)

        #for i in range(startPos[0] - int(nc/2), startPos[0] + int(nc/2) + 1):
        #    a.append(maze[i][startPos[1] - nl + 1 : startPos[1] + 1])
        #a[int(nc/2)][nl - 1] = PLAYER

        # rotate 90
        a = list(zip(*a))
        a = a[::-1]



    return a

def printWmatrix(a, dir):
    if dir == Directions.UP:
        for i in range(len(a) - 1, -1, -1):
            for j in range(len(a[i])):
                print(a[i][j], end="")
            print()

    elif dir == Directions.DOWN:
        for i in range(len(a)):
            for j in range(len(a[i])):
                print(a[i][j], end="")
            print()

    elif dir == Directions.RIGHT:
        for j in range(len(a[0]) - 1 , -1, -1):
            for i in range(len(a)):
                print(a[i][j], end="")
            print()

    elif dir == Directions.LEFT:
        for j in range(len(a[0])):
            for i in range(len(a) - 1, -1, -1):
                print(a[i][j], end="")
            print()

def nextDir(crtPos, nextPos):
    if nextPos[0] == crtPos[0] - 1:
        return Directions.UP

    if nextPos[0] == crtPos[0] + 1:
        return Directions.DOWN

    if nextPos[1] == crtPos[1] - 1:
        return Directions.LEFT

    if nextPos[1] == crtPos[1] + 1:
        return Directions.RIGHT

    return None


def debugWM(maze, start, dir, nl, nc):
    
    while True:
        maze[start[0]][start[1]] = PLAYER
        printMaze(maze)

        wm = createWorkingMatrix(maze, start, nl, nc, dir)
        print("logic view:")
        print(dir)
        printWmatrix(wm, dir)

        print("internal view:")
        print(dir)
        printMaze(wm)

        key = input()
        if key == 'q':
            break

        if key == 'w' and maze[start[0]-1][start[1]] != WALL:
            maze[start[0]][start[1]] = EMPTY
            dir = Directions.UP
            start = (start[0]-1, start[1])

        elif key == PLAYER and maze[start[0]+1][start[1]] != WALL:
            maze[start[0]][start[1]] = EMPTY
            dir = Directions.DOWN
            start = (start[0]+1, start[1])

        elif key == 'a' and maze[start[0]][start[1]-1] != WALL:
            maze[start[0]][start[1]] = EMPTY
            dir = Directions.LEFT
            start = (start[0], start[1]-1)

        elif key == 'd' and maze[start[0]][start[1]+1] != WALL:
            maze[start[0]][start[1]] = EMPTY
            dir = Directions.RIGHT
            start = (start[0], start[1]+1)

        os.system("cls")



def solveAStar(maze, start, finish):
    path = astar(maze, start, finish)
    path.insert(0, path[0])

    crtDir = Directions.UP

    for i in range(len(path) - 1, 0, -1):
        maze[path[i][0]][path[i][1]] = PLAYER
        printMaze(maze)

        wm = createWorkingMatrix(maze, path[i], 4, 4, crtDir)
        print("logic view:")
        print(crtDir)
        printWmatrix(wm, crtDir)

        print("internal view:")
        print(crtDir)
        printMaze(wm)

        time.sleep(1)
        os.system("cls")

        maze[path[i][0]][path[i][1]] = EMPTY
        crtDir = nextDir(path[i], path[i-1])

class Actions(Enum):
    DO_NOTHING = 0
    TURN_RIGHT = 1
    TURN_LEFT = 2
    MOVE_RIGHT = 3
    MOVE_LEFT = 4

from msvcrt import getch, kbhit
def getAction():
    move = ''
    if kbhit():
        move = getch()
        if ord(move) == ord('d'):
            return Actions.TURN_RIGHT
        elif ord(move) == ord('a'):
            return Actions.TURN_LEFT
        elif ord(move) == ord('j'):
            return Actions.MOVE_LEFT
        elif ord(move) == ord('l'):
            return Actions.MOVE_RIGHT

    return Actions.DO_NOTHING


def updatePlayerState(dir, pos, action):
    if action == Actions.DO_NOTHING:
        return dir, pos

    if action == Actions.TURN_RIGHT:
        if dir == Directions.UP:
            return Directions.RIGHT, pos
        
        if dir == Directions.RIGHT:
            return Directions.DOWN, pos

        if dir == Directions.DOWN:
            return Directions.LEFT, pos

        if dir == Directions.LEFT:
            return Directions.UP, pos

    elif action == Actions.TURN_LEFT:
        if dir == Directions.UP:
            return Directions.LEFT, pos

        if dir == Directions.LEFT:
            return Directions.DOWN, pos

        if dir == Directions.DOWN:
            return Directions.RIGHT, pos

        if dir == Directions.RIGHT:
            return Directions.UP, pos


    elif action == Actions.MOVE_LEFT:
        if dir == Directions.UP:
            return dir, (pos[0], pos[1]-1)

        if dir == Directions.LEFT:
            return dir, (pos[0]+1, pos[1])

        if dir == Directions.DOWN:
            return dir, (pos[0], pos[1]+1)

        if dir == Directions.RIGHT:
            return dir, (pos[0]-1, pos[1])

    elif action == Actions.MOVE_RIGHT:
        if dir == Directions.UP:
            return dir, (pos[0], pos[1]+1)

        if dir == Directions.LEFT:
            return dir, (pos[0]-1, pos[1])

        if dir == Directions.DOWN:
            return dir, (pos[0], pos[1]-1)

        if dir == Directions.RIGHT:
            return dir, (pos[0]+1, pos[1])

    return dir, pos


def play(maze, start, dir, nl, nc):
    time.sleep(1)

    crtDir = dir
    crtPos = start

    numMoves = 0;

    while True: 
        time.sleep(0.5) 
        os.system("cls") 
        
        #move = ''
        #if kbhit():
        #    move = getch()
        #    if ord(move) == ord('d'):
        #        crtDir = Directions.RIGHT
        #    elif ord(move) == ord('w'):
        #        crtDir = Directions.UP
        #    elif ord(move) == ord('a'):
        #        crtDir = Directions.LEFT
        #    elif ord(move) == ord(PLAYER):
        #        crtDir = Directions.DOWN

        maze[crtPos[0]][crtPos[1]] = EMPTY

        newDir, newPos = updatePlayerState(crtDir, crtPos, getAction())
        if numMoves > 3 and newDir != crtDir:
            numMoves = 0
            crtDir = newDir

        if maze[newPos[0]][newPos[1]] != WALL:
            crtPos = newPos

        
        
        if crtDir == Directions.UP:
            crtPos = (crtPos[0]-1, crtPos[1])
        elif crtDir == Directions.LEFT:
            crtPos = (crtPos[0], crtPos[1]-1)
        elif crtDir == Directions.DOWN:
            crtPos = (crtPos[0]+1, crtPos[1])
        elif crtDir == Directions.RIGHT:
            crtPos = (crtPos[0], crtPos[1]+1)
        
        if maze[crtPos[0]][crtPos[1]] == WALL:
            break
        
        maze[crtPos[0]][crtPos[1]] = PLAYER
        printMaze(maze)

        numMoves += 1
        
        wm = createWorkingMatrix(maze, crtPos, nl, nc, crtDir)
        print("logic view:")
        print(crtDir)
        printWmatrix(wm, crtDir)

        print("internal view:")
        print(crtDir)
        printMaze(wm)

    maze[crtPos[0]][crtPos[1]] = PLAYER
    printMaze(maze)


def main():
    maze = readMaze('maze2.txt')
    #printMaze(maze)
    findStartAndFinish(maze)

    maze[start[0]][start[1]] = PLAYER

   
    #solveAStar(maze, start, finish)

    #debugWM(maze, start, Directions.UP, 10, 10)

    #play(maze, start, Directions.UP, 5, 5)

    startDir = Directions.UP
    Qlearning(3000, 0.4, 0.1, maze, start, startDir, 5, 5)

    #state = createWorkingMatrix(maze, start, 5, 5, startDir)


    #l = list(Actions)
    #print(l)
    #print(l[0])
    #import random
    #print(random.choice(list(Actions)))

if __name__ == "__main__":
    sys.exit(int(main() or 0))
