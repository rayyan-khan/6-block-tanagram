import sys
import time
from tkinter import *

# part 1 working without rotations

#INPUTLIST = ['block.py', '4 4', '2x2', '2 2', '2 2', '2 2']  # temporary, will be replaced by sys.argv
#INPUTLIST = ['b.py', '2 4', '2 1', '2 3']
#INPUTLIST = ['b.py', '3 3', '1 1', '1 2', '2 3']
#INPUTLIST = ['b.py', '4 6', '1 1', '2 2', '1 3', '1 3', '3 1', '2 4', '2 1']
#INPUTLIST = ['b.py', '100x100', '50x50', '50x50', '50x50', '50x50']
#INPUTLIST = ['bp', '100x100'] + ['25x25' for n in range(16)]
#INPUTLIST = ['bp', '7x4', '4x7']
INPUTLIST = sys.argv

INPUT = ' '.join(INPUTLIST[1:]).replace('x', ' ').split(' ')
# input should be all numbers individually regardless of if separated by x or space
BOARDW, BOARDH = int(INPUT[1]), int(INPUT[0]) # double check this -- board width and height


# take input and create board and blocks
START = {y: ''.join(['.' for n in range(BOARDW)]) for y in range(BOARDH)}
        # dict w/ y as key and string as value
BLOCKS = {int(index/2): (INPUT[index], INPUT[index + 1]) for index in range(2, len(INPUT), 2)}
        # set of blocks represented by (width, height)
replace = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CHOICES = {key: replace[key] for key in BLOCKS}

# helper methods:
def makeBoard(width, height): # dict w/ y as key and string as value
    return {y: ''.join(['.' for n in range(width)]) for y in range(height)}

def areaAddsUp(boardw, boardh, blx):
    totalArea = boardw*boardh
    blockArea = sum([int(blx[key][0])*int(blx[key][1]) for key in blx])
    if totalArea != blockArea:
        return False
    return True

def canAdd(width, height, topLeftCorner, board, blocksIn):
    x, y = topLeftCorner
    if (x + width) > BOARDW:
        return False
    elif (y + height) > BOARDH:
        return False
    elif board[y][x:x + width].count('.') < width:
        return False
    return True

def addBlock(height, width, blockNum, topLeftCorner, board, blocksIn): # (h, w), (x + 1, y) of top left corner of block, what it gets filled with
    x, y = topLeftCorner
    marker = CHOICES[blockNum]

    # check if possible to add block:
    if canAdd(width, height, topLeftCorner, board, blocksIn):
        boardCopy = board.copy()
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
    if board == False:
        print('No solution.')
    seen = set()
    output = []
    reverseChoices = {CHOICES[key]:key for key in CHOICES}

    for key in board:
        for index in range(len(board[key])):
            label = board[key][index]
            if label in seen:
                continue
            seen.add(label)
            height, width = BLOCKS[int(reverseChoices[label])]
            if index + int(width) - 1 <= BOARDW and board[key][index + int(width) - 1] == label:
                output.append('{}x{}'.format(height, width))
            else:
                output.append('{}x{}'.format(width, height))
    return output

def solve(board, currentRow, choices, blocksIn):
    if areaAddsUp(BOARDH, BOARDW, BLOCKS):
        return solve1(board, currentRow, choices, blocksIn)
    else: return 'Blocks do not fill area.'

# method to find puzzle solution:
def solve1(board, currentRow, choices, blocksIn):
    #printBoard(board)
    if not choices:
        if filled(board):
            #printBoard(board)
            #print('solved!')
            return board

    if '.' in board[currentRow]:
        nextOpenIndex = board[currentRow].find('.')
    else:
        while '.' not in board[currentRow]:
            currentRow += 1
        nextOpenIndex = board[currentRow].find('.')

    for choice in choices:
        #print('Choice', choice)
        #printBoard(board)
        newChoices = choices.copy()
        newChoices.pop(choice)
        newBlocksIn = blocksIn.copy()
        newBlocksIn.add(str(choice))

        height, width = int(BLOCKS[choice][0]), int(BLOCKS[choice][1])
        for rotation in range(2):
            #print('Blocks in:', blocksIn)
            if rotation == 0:
                newBoard = addBlock(height, width, choice,
                                    (nextOpenIndex, currentRow), board, newBlocksIn)
                if newBoard:
                    result = solve1(newBoard, currentRow, newChoices, newBlocksIn)
                    if result:
                        return result
            if height != width and rotation == 1:
                width, height = int(BLOCKS[choice][0]), int(BLOCKS[choice][1])
                #print('At second rotation - adding h: {}, w: {}.'.format(height,width))
                #print(board)
                #printBoard(board)
                newBoard = addBlock(height, width, choice,
                                    (nextOpenIndex, currentRow), board, newBlocksIn)
                if newBoard:
                    result = solve1(newBoard, currentRow, newChoices, newBlocksIn)
                    if result:
                        return result

    return False

start = time.clock()
print(output(solve(START, 0, CHOICES, set())))
print('Total time: {} seconds.'.format(round(time.clock() - start, 3)))
