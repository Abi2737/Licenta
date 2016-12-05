from heapq import heappop, heappush

# Scrie?i o func?ie care verific? dac? un tuplu dat reprezint?
# coordonatele unei pozi?ii libere de pe hart? (coordonatele nu dep??esc limitele h?r?ii
# ?i acolo nu se g?se?te un obstacol)
def is_good(maze, pos):
    # TODO
    if pos[0] < 0 or pos[0] >= len(maze):
        return False

    if pos[1] < 0 or pos[1] >= len(maze[0]):
        return False

    if maze[pos[0]][pos[1]] == 'x':
        return False

    return True

# Scrie?i o func?ie care �ntoarce celulele vecine posi?iei date (doar cele libere)
# Folosi?i func?ionala filter ?i func?ia is_good scris? anterior
def get_neighbours(maze, pos):
    (r, c) = pos  # A?a se poate desface o pozi?ie �n componentele sale
    # TODO
    result = [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1]), (pos[0], pos[1] - 1)]

    return list(filter(lambda p: is_good(maze, p), result))

def manhattan_distance(a, b):
    # TODO
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def astar(maze, start, end):

    # openList (frontiera) ca un heap de tupluri (cost-total-estimat, nod)
    openList = []
    heappush(openList, (0 + manhattan_distance(start, end), start))

    # closedList (teritoriu) ca un dictionar nod -> (parinte, cost-real-pana-la-nod)
    closedList = {start: (None, 0)}

    realCostLabyrinth = [[0 for c in range(len(maze[0]))] for r in range(len(maze))]
    realCostLabyrinth[start[0]][start[1]] = 1;

    # cat timp mai am stari in openList (frontiera)
    while openList:
        # elimin nodul S cu f(S) minim din openList si il inserez in closedList
        (ScostEstimat, Snod) = heappop(openList)
        costParinteReal = closedList[Snod][1]

        if Snod == end:
            # TODO construieste solutia
            path = []
            while Snod is not None:
                path.append(Snod)
                Snod = closedList[Snod][0]

            return  path

        succesori_Snod = get_neighbours(maze, Snod)
        for Si in succesori_Snod:
            nodNouSiOpenL = (costParinteReal + 1 + manhattan_distance(Si, end), Si)
            nodNouSiClosedL = (Snod, costParinteReal + 1)

            if nodNouSiOpenL not in openList:
                if Si not in closedList.keys():
                    heappush(openList, nodNouSiOpenL)
                    closedList[Si] = nodNouSiClosedL

                    realCostLabyrinth[Si[0]][Si[1]] = nodNouSiClosedL[1] + 1

    return None
