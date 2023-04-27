# AIM: IMPLEMENTS SEVERAL HELPER FUNCTIONS USED FOR GETTING THE NEXT MOVE
import math
import tkinter
from operator import le
import numpy as np
from random import randint


def log2(x):
    if x<=0:
        return 0
    else:
        return int(math.log10(x) / math.log10(2))


# Gets the Child of a node in a particular direction
def getChild(grid, dir):
    temp = grid.clone()
    temp.move(dir)
    return temp


# Gets all the Children of a node
def children(grid):
    children = []
    for move in grid.getAvailableMoves():
        children.append(getChild(grid, move))
    return children


# Returns true if the node is terminal
def terminal(grid):
    return not grid.canMove()


def smoothness(grid):  # calculating the sum of the differences between adjacent numbers
    smoothness = 0
    for x in range(grid.size):
        for y in range(grid.size):
            if not grid.canInsert((x, y)):
                currCellValue = log2(grid.map[x][y])
                for direction in range(2):
                    processed = 0
                    targetCellValue = np.inf
                    if direction == 0 and not grid.crossBound((x + 1, y)) and grid.map[x + 1][y] > 0:
                        targetCellValue = log2(grid.map[x + 1][y])
                        processed = 1
                    if direction == 1 and not grid.crossBound((x, y + 1)) and grid.map[x][y + 1] > 0:
                        targetCellValue = log2(grid.map[x][y + 1])
                        processed = 1
                    if processed != 0:
                        smoothness -= abs(currCellValue - targetCellValue)  # abs(currCellValue - targetCellValue)
    return smoothness


def monotonicity(grid):  #
    totals = [0, 0, 0, 0]
    # up and down direction
    for x in range(grid.size):
        current = 0
        next = current + 1
        while (next < grid.size):
            while next < grid.size and not grid.canInsert((x, next)):
                next += 1
            if (next >= grid.size):
                next -= 1
            currentValue = 0
            if not grid.canInsert((x, current)):
                currentValue = log2(grid.map[x][current])
            nextValue = 0
            if not grid.canInsert((x, next)):
                nextValue = log2(grid.map[x][next])
            if (currentValue > nextValue):
                totals[0] += nextValue - currentValue
            elif (nextValue > currentValue):
                totals[1] += currentValue - nextValue
            current = next
            next += 1
    # right and left direction
    for y in range(grid.size):
        current = 0
        next = current + 1
        while (next < grid.size):
            while next < grid.size and not grid.canInsert((next, y)):
                next += 1
            if (next >= grid.size):
                next -= 1
            currentValue = 0
            if not grid.canInsert((current, y)):
                currentValue = log2(grid.map[current][y])
            nextValue = 0
            if not grid.canInsert((next, y)):
                nextValue = log2(grid.map[next][y])
            if (currentValue > nextValue):
                totals[2] += nextValue - currentValue
            elif (nextValue > currentValue):
                totals[3] += currentValue - nextValue
            current = next
            next += 1

    return max(totals[0], totals[1]) + max(totals[2], totals[3])


def getMaxTileLocation(grid):  # get the location of the biggest number
    maxTileLocation = []
    maxTile = 0
    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] > maxTile:
                maxTile = grid.map[x][y]
                maxTileLocation.append((x, y))

    return maxTileLocation


def getRankedValueLocationDir(grid):  # Sort the numbers on the board from smallest to largest
    dir = {}
    maxTile = 0
    for x in range(grid.size):
        for y in range(grid.size):
            if not grid.canInsert((x, y)):
                dir[grid.map[x][y]] = (x, y)  # index:number value:location
    return dir


def isBigTileInCorner(grid):  # whether the biggest number is in the corner
    currLocaList = getMaxTileLocation(grid)
    inCorner = 0
    for currLoca in currLocaList:
        if currLoca == (grid.size - 1, grid.size - 1) or currLoca == (0, 0) or currLoca == (
                0, grid.size - 1) or currLoca == (grid.size - 1, 0):
            inCorner = 1
    if inCorner == 1:
        return True
    else:
        return False


def getAverageScorePerGrid(grid):  # average of all the grids
    total = 0
    CellNum = 0
    for x in range(grid.size):
        for y in range(grid.size):
            if not grid.canInsert((x, y)):
                total += grid.map[x][y]
                CellNum += 1
    if CellNum == 0:
        return 0
    else:
        return float(total) / CellNum


def getAverageScorePerGrid_tail(grid):  # average of the grids with numbers
    numberIncluded = 12
    rankDir = getRankedValueLocationDir(grid)
    total = 0
    CellNum = 0
    i = 0
    for index in sorted(rankDir):
        i += 1
        if i <= numberIncluded:
            if index != 0:
                total += index
                CellNum += 1
    if CellNum == 0:
        return 0
    else:
        return float(total) / CellNum


def biggerTilesOnBoarderPreference(grid):  # four of the bigger number is on the side
    numberIncluded = 4
    rankDir = getRankedValueLocationDir(grid)
    total = 0
    i = 0
    for index in reversed(sorted(rankDir)):
        i += 1
        if i <= numberIncluded:
            if index != 0:
                if rankDir[index][0] == 0 or rankDir[index][0] == grid.size - 1 or rankDir[index][1] == 0 or \
                        rankDir[index][1] == grid.size - 1:
                    total += index
    return float(total)


# Evaluates the heuristic. The heuristic used here is a gradient function
def Eval1(grid):
    if terminal(grid):
        return -np.inf

    gradients = [
        [[3, 2, 1, 0], [2, 1, 0, -1], [1, 0, -1, -2], [0, -1, -2, -3]],
        [[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, -0]],
        [[0, -1, -2, -3], [1, 0, -1, -2], [2, 1, 0, -1], [3, 2, 1, 0]],
        [[-3, -2, -1, 0], [-2, -1, 0, 1], [-1, 0, 1, 2], [0, 1, 2, 3]]
    ]

    values = [0, 0, 0, 0]

    for i in range(4):
        for x in range(4):
            for y in range(4):
                values[i] += gradients[i][x][y] * grid.map[x][y]

    eval1 = max(values)
    return eval1


def Eval2(grid):
    emptyCellNum = len(grid.getAvailableCells())
    if emptyCellNum == 0:
        emptyCellNum = 1
    biggestTileInCorner = -1000
    smoothWeight = 10.5
    monoWeight = 19.5
    emptyWeight = 5
    maxWeight = 500
    averageWeight = 250
    biggerTileOnBoaderWeight = 2

    eval2 = smoothness(grid) * smoothWeight \
            + monotonicity(grid) * monoWeight \
            + grid.getMaxTile() * maxWeight \
            + emptyCellNum * emptyWeight \
            + getAverageScorePerGrid_tail(grid) * averageWeight \
            + (1 - isBigTileInCorner(grid)) * biggestTileInCorner \
            + biggerTilesOnBoarderPreference(grid) * biggerTileOnBoaderWeight
    return eval2


def draw_board(canvas, data):
    # Background
    canvas.create_rectangle(0, 0, 600, 600, fill=data.game_bg_color, width=0)
    # print(data.grid.size)

    # Tiles
    for i in range(data.grid.size):
        for j in range(data.grid.size) :
            # Coordinates
            x1 = data.thick * (j + 1) + data.size * j
            y1 = data.thick * (i + 1) + data.size * i
            x2 = x1 + data.size
            # print(x2)
            y2 = y1 + data.size
            # Label
            # print(data.grid.map[i][j])
            tile_color = data.tile_color[log2(data.grid.map[i][j])]
            text_color = data.dark_text_color if log2(data.grid.map[i][j]) < 3 else data.light_text_color
            text = "" if data.grid.map[i][j] == 0 else str(data.grid.map[i][j])
            # Draw
            canvas.create_rectangle(x1, y1, x2, y2, fill=tile_color, width=0)
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=("Open Sans", "55", "bold"),
                               fill=text_color)


def draw_over(canvas, data):
    # Background
    canvas.create_rectangle(0, 0, 600, 600, fill=data.end_bg_color, width=0)
    # Text
    text = "GAME OVER :)\n\nYOUR SCORE: " + str(data.grid.getMaxTile())

    canvas.create_text(600/2, 600/2, text=text, font=("Open Sans", "60", "bold"), fill=data.light_text_color)


def rgb2hex(r, g, b):
    '''
    Converts RGB color code to hex for tiles
    '''
    return '#%02x%02x%02x' % (r, g, b)




