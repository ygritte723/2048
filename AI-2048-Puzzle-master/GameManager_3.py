from tkinter import ALL

from Grid_3 import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_3 import PlayerAI
from Displayer_3 import Displayer
from Helper import draw_board, rgb2hex, draw_over
from random import randint
import time
import tkinter

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)
turn = 0

# Time Limit Before Losing
timeLimit = 0.9
allowance = 0.05


def timerFired(self):
    global maxTile
    global turn
    if not self.isGameOver() and not self.over:
        # Copy to Ensure AI Cannot Change the Real Grid to Cheat
        gridCopy = self.grid.clone()
        # print(gridCopy.map)
        move = None

        if turn == 0:
            print("Player's Turn:")
            # print("Player's Turn:")
            move = self.playerAI.getMove(gridCopy)
            print(actionDic[move])
            # print(move)
            # Validate Move
            if move is not None and 0 <= move < 4:
                if self.grid.canMove([move]):
                    self.grid.move(move)
                    # Update maxTile
                    maxTile = self.grid.getMaxTile()
                    print(maxTile)
                else:
                    print("Invalid PlayerAI Move!\n")
                    print(move)
                    print(actionDic[move])
                    print(self.grid.map)
                    self.over = True
            else:
                print("Invalid PlayerAI Move - 1")
                print(move)
                print(actionDic[move])
                print(self.grid.map)
                self.over = True
            #time.sleep(1)
        else:
            print("Computer's turn:")  
            gridCopy = self.grid.clone()
            move = self.computerAI.getMove(gridCopy)
            # Validate Move
            if move and self.grid.canInsert(move):
                self.grid.setCellValue(move, self.getNewTileValue())
            else:
                print("Invalid Computer AI Move!\n")
                print(move)
                print(actionDic[move])
                print(self.grid.map)
                self.over = True    
        
        turn = 1-turn
        

        # Exceeding the Time Allotted for Any Turn Terminates the Game
        if not self.mode:
            self.updateAlarm(time.perf_counter())

    #print(maxTile)


def timerFiredWrapper(canvas, data):
    redrawAllWrapper(canvas, data)
    timerFired(data)
    canvas.after(200, timerFiredWrapper, canvas, data)


def redrawAll(canvas, data):
    if data.over:
        draw_over(canvas, data)
    else:
        draw_board(canvas, data)


def redrawAllWrapper(canvas, data):
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, 600, 600,
                            fill='white', width=0)
    redrawAll(canvas, data)
    canvas.update()


class GameManager:
    def __init__(self, size=4):
        self.prevTime = time.perf_counter()
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles = defaultInitialTiles
        self.computerAI = None
        self.playerAI = None
        self.displayer = None
        self.over = False
        self.mode = 0

        # Sizes
        self.size = 600 / (1.12 * self.grid.size)
        self.thick = self.size / 10

        # Colors
        self.game_bg_color = rgb2hex(187, 173, 161)
        self.end_bg_color = rgb2hex(241, 196, 15)

        self.dark_text_color = rgb2hex(118, 110, 101)
        self.light_text_color = rgb2hex(249, 246, 242)

        self.tile_color = [
            rgb2hex(205, 192, 181),  # None
            rgb2hex(238, 228, 218),  # 2
            rgb2hex(237, 224, 200),  # 4
            rgb2hex(242, 177, 121),  # 8
            rgb2hex(245, 149, 99),  # 16
            rgb2hex(246, 124, 95),  # 32
            rgb2hex(246, 94, 59),  # 64
            rgb2hex(237, 207, 114),  # 128
            rgb2hex(237, 204, 97),  # 256
            rgb2hex(237, 200, 80),  # 512
            rgb2hex(237, 197, 63),  # 1024
            rgb2hex(237, 194, 46),  # 2048
            rgb2hex(237, 190, 42)  # 4096
        ]

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
            pass
        else:
            while time.perf_counter() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.perf_counter()

    def start(self):
        self.prevTime = time.perf_counter()
        for i in range(self.initTiles):
            self.insertRandonTile()
        root = tkinter.Tk()
        canvas = tkinter.Canvas(root, width=600, height=600)
        canvas.pack()
        root.title("2048")

        timerFiredWrapper(canvas, self)

        # puts everything on the display,
        # and responds to user input until the program terminates
        root.mainloop()

        # timerFiredWrapper(canvas, self)

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0, 99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)


def main():
    size = int(input("please enter the size of grid:"))
    gameManager = GameManager(size)
    playerAI = PlayerAI()
    computerAI = ComputerAI()
    displayer = Displayer()
    mode = int(input("please enter the game mode(0 for auto mode and 1 for player mode):"))
    gameManager.mode = mode
    computerAI.mode = mode
    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)

    gameManager.start()


if __name__ == '__main__':
    main()
