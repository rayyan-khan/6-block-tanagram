import sys
import time
from tkinter import *

# trying to add rotations
# fix output

#INPUTLIST = ['block.py', '4 4', '2x2', '2 2', '2 2', '2 2']  # temporary, will be replaced by sys.argv
#INPUTLIST = ['b.py', '2 4', '2 1', '2 3']
#INPUTLIST = ['b.py', '3 3', '1 1', '1 2', '2 3']
#INPUTLIST = ['b.py', '4 6', '1 1', '2 2', '1 3', '1 3', '3 1', '2 4', '2 1']
#INPUTLIST = ['b.py', '100x100', '50x50', '50x50', '50x50', '50x50']
#INPUTLIST = ['bp', '100x100'] + ['25x25' for n in range(16)]
#INPUTLIST = ['bp', '7x4', '4x7']
INPUTLIST =  sys.argv
print(INPUTLIST)

INPUT = ' '.join(INPUTLIST[1:]).replace('x', ' ').split(' ')
# input should be all numbers individually regardless of if separated by x or space
BOARDW, BOARDH = int(INPUT[1]), int(INPUT[0]) # double check this -- board width and height


# take input and create board and blocks
START = {y: ''.join(['.' for n in range(BOARDW)]) for y in range(BOARDH)}
        # dict w/ y as key and string as value
initBlocks = {int(index/2): (INPUT[index], INPUT[index + 1]) for index in range(2, len(INPUT), 2)}
rblocks = {str(int(index/2)) + 'r': (INPUT[index + 1], INPUT[index]) for index in range(2, len(INPUT), 2)}
BLOCKS = {**initBlocks, **rblocks}
        # set of blocks represented by (width, height)
replace = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
initChoices = {key: replace[key] for key in BLOCKS if type(key) == int}
rChoices = {key: replace[int(key[0])] for key in BLOCKS if type(key) == str}
CHOICES = {**initChoices, **rChoices}
print(CHOICES)

# helper methods:
def makeBoard(width, height): # dict w/ y as key and string as value
    return {y: ''.join(['.' for n in range(width)]) for y in range(height)}

def areaAddsUp(boardw, boardh, blx):
    totalArea = boardw*boardh
    print('totalArea', totalArea)
    blockArea = sum([int(blx[key][0])*int(blx[key][1]) for key in blx])*.5
    print('block area', blockArea)
    if totalArea != blockArea:
        return False
    return True

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
    if type(blockNum) == str:
        blockNum = int(blockNum[0])
        width, height = int(BLOCKS[blockNum][0]), int(BLOCKS[blockNum][1])
    else:
        height, width = int(BLOCKS[blockNum][0]), int(BLOCKS[blockNum][1])
    marker = CHOICES[blockNum]

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
    if BOARDW > 30: print('\n')
    else: print('')

def output(board):
    seen = set()
    output = []
    reverseChoices = {CHOICES[key]:key for key in CHOICES}
    for key in board:
        for label in board[key]:
            if label in seen:
                continue
            seen.add(label)
            height, width = BLOCKS[int(reverseChoices[label])]
            output.append('{}x{}'.format(height, width))
    return output

def solve(board, currentRow, choices, blocksIn):
    if areaAddsUp(BOARDH, BOARDW, BLOCKS):
        return solve1(board, currentRow, choices, blocksIn)
    else: return 'Blocks do not fill area.'

# method to find puzzle solution:
def solve1(board, currentRow, choices, blocksIn):
    printBoard(board)
    if not choices:
        if filled(board):
            printBoard(board)
            print('solved!')
            #return output(board)
            return board

    if '.' in board[currentRow]:
        nextOpenIndex = board[currentRow].find('.')
    else:
        while '.' not in board[currentRow]:
            currentRow += 1
        nextOpenIndex = board[currentRow].find('.')

    for choice in choices:
        print(choice)
        newChoices = choices.copy()
        newChoices.pop(choice) # take out choice
        newBlocksIn = blocksIn.copy()
        newBlocksIn.add(str(choice))
        newBoard = addBlock(choice, (nextOpenIndex, currentRow), board, newBlocksIn)
        if newBoard == False:
            continue
        withoutRotation = newChoices.copy()
        withoutRotation.pop(str(choice) + 'r')
        result = solve1(newBoard, currentRow, withoutRotation, newBlocksIn)
        if result == False:
            result = solve1(newBoard, currentRow, newChoices, newBlocksIn)
        return result

    return 'No solution.'

print(solve(START, 0, CHOICES, set()))
