import sys
import time
from tkinter import *

INPUTLIST = ['block.py', '4 4', '2x2', '2 2', '2 2', '2 2']  # temporary, will be replaced by sys.argv
INPUT = ' '.join(INPUTLIST[1:]).replace('x', ' ').split(' ')
# input should be all numbers individually regardless of if separated by x or space
BOARDW, BOARDH = int(INPUT[1]), int(INPUT[0]) # double check this -- board width and height

# take input and create board and blocks
BOARD = {y: ''.join(['.' for n in range(BOARDW)]) for y in range(BOARDH)}
        # dict w/ y as key and string as value
BLOCKS = {index/2: (INPUT[index], INPUT[index + 1]) for index in range(2, len(INPUT), 2)}
        # set of blocks represented by (width, height)

# helper methods:
def printBoard():
    for key in BOARD:
        print(' '.join(BOARD[key]))
    print('\n')

def overlap(width, height, topLeftCorner):
    x, y = topLeftCorner
    for dep in range(y, y + height):
        if '1' in BOARD[y][x:x + width + 1]: # figure out a better way
            return True
    return False

def addBlock(blockNum, topLeftCorner): # (w, h), (x + 1, y) of top left corner of block,
                                         # what it gets filled with
    x, y = topLeftCorner
    width, height = int(BLOCKS[blockNum][0]), int(BLOCKS[blockNum][1])
    marker = str(blockNum)

    # check if possible:
    if (x + width) > BOARDW:
        return False
    elif (y + height) > BOARDH:
        return False
    elif overlap(width, height, topLeftCorner):
        print('overlaps')
        return False

    for dep in range(y, y + height):
        BOARD[dep] = BOARD[dep][0:x] + marker*width + BOARD[dep][x + width:]

addBlock(1, (0,0))
printBoard()
addBlock(2, (1, 1))
