# Jeffrey Luo (jl834)
# Nathan Kim (njk24)

import csv
import numpy as np
import math 

counter = 0 # number of non-zero elements
vector = [] # squashed vector

# 1D DCT helper
def DCT_helper(list, index):
    output = 0
    for x in range(8):
        output += list[x] * np.cos((math.pi/8)*(x+0.5)*index)
    return output

# 2D DCT
def DCT(x, y):
    # first do the row transform
    newblock = []
    outputblock = []
    outputblockinverse = [[0 for i in range(8)] for j in range(8)]
    for row in range(x, x + 8):
        rowdata = [data[row][y], data[row][y+1], data[row][y+2], data[row][y+3], data[row][y+4], data[row][y+5], data[row][y+6], data[row][y+7]]
        newlist = [DCT_helper(rowdata, 0), DCT_helper(rowdata, 1), DCT_helper(rowdata, 2), DCT_helper(rowdata, 3), DCT_helper(rowdata, 4), DCT_helper(rowdata, 5), DCT_helper(rowdata, 6), DCT_helper(rowdata, 7)]
        newblock.append(newlist)
    # column transform
    for col in range(8):
        coldata = [newblock[0][col], newblock[1][col], newblock[2][col], newblock[3][col], newblock[4][col], newblock[5][col], newblock[6][col], newblock[7][col]]
        newlist = [DCT_helper(coldata, 0), DCT_helper(coldata, 1), DCT_helper(coldata, 2), DCT_helper(coldata, 3), DCT_helper(coldata, 4), DCT_helper(coldata, 5), DCT_helper(coldata, 6), DCT_helper(coldata, 7)]
        outputblock.append(newlist)
    for x in range(8):
        for y in range(8):
            outputblockinverse[x][y] = outputblock[y][x]
    return outputblockinverse

def Quantize(qfactor, matrix):
    global counter
    global vector
    output = [[0 for i in range(8)] for j in range(8)]
    for x in range(8):
        for y in range(8):
            output[x][y] = int((matrix[x][y] / quant[x][y]) / qfactor)
            vector.append(output[x][y])
            if(output[x][y] != 0):
                counter += 1
    return output

# 
def Scan():
    rowblocks = len(data) / 8
    colblocks = len(data[0]) / 8
    qfactor = 4

    for x in range(rowblocks):
        for y in range(colblocks):
            quantizedblock = Quantize(qfactor, DCT(x * 8, y * 8))


def Encode():
    rl_encoding = []
    curr_num = vector[0]
    curr_count = 0
    for i in range(len(vector)):
        if curr_num != vector[i] or i == len(vector) - 1:
            rl_encoding.append([curr_num, curr_count])
            curr_count = 0
            curr_num = vector[i]
        curr_count += 1
    return rl_encoding

data = []

with open('parrot.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append([int(val) for val in row])
quant = []
with open('quant.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        quant.append([int(val) for val in row])

Scan()
# number of non-zero numbers
print(counter)
print(200 * 144)
# number of pairs
print(len(Encode()))


