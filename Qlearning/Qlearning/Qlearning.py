import sys
import time
import os
import random
from Game import *

DEAD_REWARD = -1

def argMax(Q, state):
    
    dicActionsReward = Q.get(state)
    
    if dicActionsReward is None:
        # nu sunt actiuni incercate pentru starea aceasta => intorc una random
        return random.choice(list(Actions)[:3]), 0
     
    # introc o actiune random din cele care au recompensa cea mai mare
    maxReward = -float('inf')
    listActionsMaxReward = []
    
    for actKey in dicActionsReward.keys():
        crtReward = dicActionsReward[actKey]
        if crtReward > maxReward:
            maxReward = crtReward
            listActionsMaxReward = [actKey]
        
        elif crtReward == maxReward:
            listActionsMaxReward.append(actKey)

    if maxReward > 0:
        # intorc actiunea cu recompensa maxima
        #print("ARG MAAAAAX", maxReward)
        #print()
        return random.choice(listActionsMaxReward), maxReward

    savedAct = listActionsMaxReward[0]

    # daca recompensa maxima este din actiunile pe care nu le-am incercat pana acum
    # (actiunile alese din starea curenta de pana acum au dus la recompense negative)
    listActionsMaxReward = list(Actions)[:3]
    for actKey in dicActionsReward.keys():
        listActionsMaxReward.remove(actKey)

    # intorc o actiune random din cele pe care nu le-am incercat
    if len(listActionsMaxReward) > 0:
        return random.choice(listActionsMaxReward), 0

    return savedAct, maxReward

def epsGreedy(Q, eps, state):
    if random.random() < eps:
        #print("RANDOM")
        #print()
        return random.choice(list(Actions)[:3])
    
    a, r = argMax(Q, state)
    return a


def turnRight(dir):
    if dir == Directions.UP:
        return Directions.RIGHT

    if dir == Directions.RIGHT:
        return Directions.DOWN

    if dir == Directions.DOWN:
        return Directions.LEFT

    return Directions.UP

def turnLeft(dir):
    if dir == Directions.UP:
        return Directions.LEFT

    if dir == Directions.LEFT:
        return Directions.DOWN

    if dir == Directions.DOWN:
        return Directions.RIGHT

    return Directions.UP

def moveLeft(dir, pos):
    if dir == Directions.UP:
        return (pos[0], pos[1]-1)

    if dir == Directions.LEFT:
        return (pos[0]+1, pos[1])

    if dir == Directions.DOWN:
        return (pos[0], pos[1]+1)

    return (pos[0]-1, pos[1])

def moveRight(dir, pos):
    if dir == Directions.UP:
        return (pos[0], pos[1]+1)

    if dir == Directions.LEFT:
        return (pos[0]-1, pos[1])

    if dir == Directions.DOWN:
        return (pos[0], pos[1]-1)

    return (pos[0]+1, pos[1])

def moveForward(dir, pos):
    if dir == Directions.UP:
        return (pos[0]-1, pos[1])

    if dir == Directions.LEFT:
        return (pos[0], pos[1]-1)

    if dir == Directions.DOWN:
        return (pos[0]+1, pos[1])
    
    return (pos[0], pos[1]+1)

def applyActions(maze, dir, pos, action):
    newDir = dir
    newPos = pos

    if action == Actions.TURN_RIGHT:
        newDir = turnRight(dir)

    elif action == Actions.TURN_LEFT:
        newDir = turnLeft(dir)

    elif action == Actions.MOVE_LEFT:
        newPos = moveLeft(dir, pos)

    elif action == Actions.MOVE_RIGHT:
        newPos = moveRight(dir, pos)

    # jocul te muta automat o casuta inainte
    newPos = moveForward(newDir, newPos)

    return newDir, newPos
    

def getReward(maze, pos):
    # calculeaza recompensa primita din noua stare
    if pos[0] < 0 or pos[0] > len(maze) or pos[1] < 0 or pos[1] > len(maze[1]):
        return DEAD_REWARD, True

    if maze[pos[0]][pos[1]] == WALL:
        return DEAD_REWARD, True
    
    return 0.01, False

def getNextStateReward(Q, state):
    dicActionsReward = Q.get(state)
    
    if dicActionsReward is None:
        # nu sunt actiuni incercate pentru starea aceasta => intorc recompensa 0
        return 0

    # introc recompensa cea mai mare
    maxReward = -float('inf')
    
    for actKey in dicActionsReward.keys():
        crtReward = dicActionsReward[actKey]
        if crtReward > maxReward:
            maxReward = crtReward

    return maxReward

def transfStateToHashableType(state):
    
    result = ""

    for i in range(len(state)):
        for j in range(len(state[i])):
            result += state[i][j]

    return result


def Qlearning(maxEp, eps, alpha, maze, startPos, startDir, nlWM, ncWM):
    Q = {}

    pauseSleep = 0.1
    
    for ep in range(maxEp):
        #####
        maze[startPos[0]][startPos[1]] = PLAYER
        #####
        state = createWorkingMatrix(maze, startPos, nlWM, ncWM, Directions.UP)
        state = transfStateToHashableType(state)
        dir = startDir
        pos = startPos
        dead = False

        #####
        numMoves = 0
        #####

        epReward = 0

        while not dead:

            
            #####
            if ep < 2000:
                #eps = 0.1
                #pauseSleep = 0.3
                time.sleep(pauseSleep) 
                os.system("cls")

            maze[pos[0]][pos[1]] = EMPTY
            #####

            action = epsGreedy(Q, eps, state)

            #####
            #if action == Actions.DO_NOTHING:
            #    numMoves = 3

            if numMoves != 0:
                action = Actions.DO_NOTHING
            #####

            newDir, newPos = applyActions(maze, dir, pos, action)
            reward, dead = getReward(maze, newPos)

            #####
            maze[newPos[0]][newPos[1]] = PLAYER
            #####
            newState = createWorkingMatrix(maze, newPos, nlWM, ncWM, newDir)
            newState = transfStateToHashableType(newState)
            newStateMaxReward = getNextStateReward(Q, newState)

            epReward += reward

            if state in Q:
                if action in Q[state]:
                    Q[state][action] = (1 - alpha) * Q[state][action] + alpha * (reward + newStateMaxReward)
                else:
                    Q[state][action] = alpha * (reward + newStateMaxReward)
            else:
                Q[state] = {}
                Q[state][action] = alpha * (reward + newStateMaxReward)

            #####
            if ep < 2000:
                maze[newPos[0]][newPos[1]] = PLAYER
                printMaze(maze)

            numMoves += 1
            if numMoves > 3:
                numMoves = 0

            if ep < 2000:
                print("numMoves: ", numMoves)
                print("Action: ", action)
                print("Ep: ", ep);

                wm = createWorkingMatrix(maze, newPos, nlWM, ncWM, newDir)
                print("logic view:")
                print(newDir)
                printWmatrix(wm, newDir)

            #print("internal view:")
            #print(newDir)
            #printMaze(wm)
            #####

            state = newState
            dir = newDir
            pos = newPos

        #####
        #print("DEAD")
        #time.sleep(pauseSleep) 

        print(epReward)

        maze[newPos[0]][newPos[1]] = WALL
        #####
