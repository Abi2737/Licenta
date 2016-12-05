import sys
import time
import os
from Astar import astar

def readMaze():
    lines = [line.rstrip('\n') for line in open('maze.txt')]

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
    if dir == 'up':
        for i in range(nl):
            a.append(maze[startPos[0] - i][startPos[1] - int(nc/2) : startPos[1] + int(nc/2) + 1])

        a[0][int(nc/2)] = 's'

    elif dir == 'down':
        for i in range(nl):
            a.append(maze[startPos[0] + i][startPos[1] - int(nc/2) : startPos[1] + int(nc/2) + 1])

        a[0][int(nc/2)] = 's'
        
    elif dir == "right":
        for i in range(startPos[0] - int(nc/2), startPos[0] + int(nc/2) + 1):
            a.append(maze[i][startPos[1] : startPos[1] + nl])

        a[int(nc/2)][0] = 's'

        # rotate 90
        a = list(zip(*a[::-1]))

    elif dir == "left":
        for i in range(startPos[0] - int(nc/2), startPos[0] + int(nc/2) + 1):
            a.append(maze[i][startPos[1] - nl + 1 : startPos[1] + 1])

        a[int(nc/2)][nl - 1] = 's'

        # rotate 90
        a = list(zip(*a))
        a = a[::-1]



    return a

def printWmatrix(a, dir):
    if dir == "up":
        for i in range(len(a) - 1, -1, -1):
            for j in range(len(a[i])):
                print(a[i][j], end="")
            print()

    elif dir == "down":
        for i in range(len(a)):
            for j in range(len(a[i])):
                print(a[i][j], end="")
            print()

    elif dir == "right":
        for j in range(len(a[0]) - 1 , -1, -1):
            for i in range(len(a)):
                print(a[i][j], end="")
            print()

    elif dir == "left":
        for j in range(len(a[0])):
            for i in range(len(a) - 1, -1, -1):
                print(a[i][j], end="")
            print()

def nextDir(crtPos, nextPos):
    if nextPos[0] == crtPos[0] - 1:
        return "up"

    if nextPos[0] == crtPos[0] + 1:
        return "down"

    if nextPos[1] == crtPos[1] - 1:
        return "left"

    if nextPos[1] == crtPos[1] + 1:
        return "right"

    return None

def main():
    maze = readMaze()
    #printMaze(maze)
    findStartAndFinish(maze)

    maze[start[0]][start[1]] = "."

    #dir = "up"
    #wm = createWorkingMatrix(maze, start, 4, 4, dir)
    #printWmatrix(wm, dir)
    #print(wm[0])
    #print(wm[1])
    #print(wm[2])    
    #print(wm[3])

    path = astar(maze, start, finish)
    path.insert(0, path[0])

    crtDir = "up"

    for i in range(len(path) - 1, 0, -1):
        maze[path[i][0]][path[i][1]] = 's'
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

        maze[path[i][0]][path[i][1]] = '.'
        crtDir = nextDir(path[i], path[i-1])

    

if __name__ == "__main__":
    sys.exit(int(main() or 0))
