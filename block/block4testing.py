import sys
import time
from tkinter import *

# adding correctly formatted output to v2, still printing though
# doesn't account for rotating blocks
# write an areaAddsUp method
# make block indexes over 10 hex or smth

#INPUTLIST = ['block.py', '4 4', '2x2', '2 2', '2 2', '2 2']  # temporary, will be replaced by sys.argv
#INPUTLIST = ['b.py', '2 4', '2 1', '2 3']
#INPUTLIST = ['b.py', '3 3', '1 1', '1 2', '2 3']
#INPUTLIST = ['b.py', '4 6', '1 1', '2 2', '1 3', '1 3', '3 1', '2 4', '2 1']
#INPUTLIST = ['b.py', '100x100', '50x50', '50x50', '50x50', '50x50']
INPUTLIST = ['bp', '100x100'] + ['25x25' for n in range(16)]
print(INPUTLIST)

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

def canAdd(width, height, topLeftCorner, board, blocksIn):
    x, y = topLeftCorner
    if (x + width) > BOARDW:
        return False
    elif (y + height) > BOARDH:
        return False
    for dep in range(y, y + height):
        if blocksIn:
            for block in blocksIn:
                if block in board[y][x:x + width]: # figure out a better way?
                    return False
        else: continue
    return True

def addBlock(blockNum, topLeftCorner, board, blocksIn): # (h, w), (x + 1, y) of top left corner of block, what it gets filled with
    x, y = topLeftCorner
    height, width = int(BLOCKS[blockNum][0]), int(BLOCKS[blockNum][1])
    marker = str(blockNum)

    # check if possible to add block:
    if canAdd(width, height, topLeftCorner, board, blocksIn):
        boardCopy = board
        for dep in range(y, y + height):
            boardCopy[dep] = board[dep][0:x] + marker*width + board[dep][x + width:]
        return boardCopy

    return False # if the block doesn't fit in this space

def filled(board):
    for key in board:
        if '.' in board[key]: return False
    return True

def printBoard(board):
    for key in board:
        print(' '.join(board[key]))

def output(board):
    seen = set()
    output = []
    for key in board:
        for label in board[key]:
            if label in seen:
                continue
            seen.add(label)
            height, width = BLOCKS[int(label)]
            output.append('{}x{}'.format(height, width))
    return output


# method to find puzzle solution:
def solve(board, currentRow, choices, blocksIn):
    printBoard(board)
    if not choices:
        if filled(board):
            printBoard(board)
            print('solved!')
            return output(board)

    if '.' in board[currentRow]:
        nextOpenIndex = board[currentRow].find('.')
    else:
        while '.' not in board[currentRow]:
            currentRow += 1
        nextOpenIndex = board[currentRow].find('.')

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

    return 'No solution.'


print(solve(START, 0, CHOICES, set()))
