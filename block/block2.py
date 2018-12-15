import sys
import time
from tkinter import *

# solves 2x2 blocks

INPUTLIST = ['block.py', '4 4', '2x2', '2 2', '2 2', '2 2']  # temporary, will be replaced by sys.argv
INPUT = ' '.join(INPUTLIST[1:]).replace('x', ' ').split(' ')
# input should be all numbers individually regardless of if separated by x or space
BOARDW, BOARDH = int(INPUT[1]), int(INPUT[0]) # double check this -- board width and height

# take input and create board and blocks
START = {y: ''.join(['.' for n in range(BOARDW)]) for y in range(BOARDH)}
        # dict w/ y as key and string as value
BLOCKS = {int(index/2): (INPUT[index], INPUT[index + 1]) for index in range(2, len(INPUT), 2)}
        # set of blocks represented by (width, height)
CHOICES = {key for key in BLOCKS}

# helper methods:
def makeBoard(width, height): # dict w/ y as key and string as value
    return {y: ''.join(['.' for n in range(width)]) for y in range(height)}

def printBoard(board):
    for key in board:
        print(' '.join(board[key]))
    print('\n')

def filled(board):
    for key in board:
        if 0 in board[key]: return False
    return True

def canAdd(width, height, topLeftCorner, board, blocksIn):
    x, y = topLeftCorner
    if (x + width) > BOARDW:
        print('too wide')
        return False
    elif (y + height) > BOARDH:
        print('too tall')
        return False
    for dep in range(y, y + height):
        if blocksIn:
            for block in blocksIn:
                if block in board[y][x:x + width + 1]: # figure out a better way?
                    return False
        else: continue
    return True

def addBlock(blockNum, topLeftCorner, board, blocksIn): # (w, h), (x + 1, y) of top left corner of block, what it gets filled with
    x, y = topLeftCorner
    width, height = int(BLOCKS[blockNum][0]), int(BLOCKS[blockNum][1])
    marker = str(blockNum)

    # check if possible to add block:
    if canAdd(width, height, topLeftCorner, board, blocksIn):
        boardCopy = board
        for dep in range(y, y + height):
            boardCopy[dep] = board[dep][0:x] + marker*width + board[dep][x + width:]
        return boardCopy

    print('cant add')
    return False # if the block doesn't fit in this space

def solve(board, currentRow, choices, blocksIn):
    printBoard(board)
    if not choices:
        print('solved!')
        return board

    if '.' in board[currentRow]:
        nextOpenIndex = board[currentRow].find('.')
    else:
        nextOpenIndex = 0
        while '.' not in board[currentRow]:
            currentRow += 1

    for choice in choices:
        newChoices = choices.copy()
        newChoices.remove(choice)
        newBlocksIn = blocksIn.copy()
        newBlocksIn.add(str(choice))
        newBoard = addBlock(choice, (nextOpenIndex, currentRow), board, newBlocksIn)
        if newBoard == False:
            continue
        result = solve(newBoard, currentRow, newChoices, newBlocksIn)
        return result

    print('failure')
    return False


print(solve(START, 0, CHOICES, set()))
