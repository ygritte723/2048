from random import randint
from BaseAI_3 import BaseAI

class ComputerAI(BaseAI):
    def __init__(self, mode = 0):
        self.mode = 0
    def getMove(self, grid):
        if (self.mode == 0):
            cells = grid.getAvailableCells()
            return cells[randint(0, len(cells) - 1)] if cells else None
        else:
            cells = []
            x,y =map(int,input("please enter the position to insert a tile( 0,0  on the bottom left corner):").split(","))
            while not grid.canInsert((int(grid.size)-y-1,x)):
                print("Invalid position")
                x,y =map(int,input("please enter the position to insert a tile( 0,0  on the bottom left corner):").split(","))
            cells.append((int(grid.size)-y-1,x))
            return cells[0]
            
