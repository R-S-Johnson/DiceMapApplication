"""
dicemap.py

Goal: Create a probability map of multi-dice summed outputs.
Usable for comparisons of probabilities. Allow interaction
with user to visualize live changes in inputs. Logic should
be based on math easier for a computer to do quickly, don't
model every possible output and count, find patterns.

Back-end logic: Multi-dice rolling can be abstracted
to recursive addition of offsetted double dice rolls.
For example: 1d3 + 2d4
                        2 3 4 5 6 7 8 9 10 (summed total)
2d4 has a count map of [1 2 3 4 3 2 1]
Add 3 together w/ offset [1 2 3 4 3 2 1]
(with padded zeros)        [1 2 3 4 3 2 1]
count map of 3 4 4 ->  [1 3 6 9 10 9 6 3 1]
Divide each by max num of possible output to get final
probability.

Created by: Winter Johnson on 6/7/23
"""

import matplotlib.pyplot as plt
from operator import mul
from functools import reduce
import time
import math

"""
Insert list of dice to be roled as ints rep max face value:
1d4 + 2d6 -> [4, 6, 6] (order unimportant).
"""
def diceMap(diceList, rec=False):
    # responsible for recording the number of times each value appears
    probArray = [0]*(sum(diceList)-len(diceList)+1)

    # Total number of possible outcomes (product of input)
    div = reduce(mul, diceList)


    if len(diceList) == 1: # 1 dice, easy probability
        return [1/diceList[0] for _ in range(diceList[0])]
    
    elif len(diceList) > 2: # recursive case

        # rec=true returns the count map (not probability)
        tmp = diceMap(diceList=diceList[1:], rec=True)

        # performs back-end logic
        for probOffset in range(diceList[0]):
            for placeIndex in range(len(tmp)):
                probArray[placeIndex + probOffset] += tmp[placeIndex]

    else: # Base case, 2 dice
        probArray = doubleDiceCall(diceList[0], diceList[1])

    if rec:
        return probArray
    return [i/div for i in probArray]

"""
Helper function for above. Only needs to return
count map of 2 dice rolling
   1 2 3 4 . .
   -------
1| 2 3 4 5
2| 3 4 5 6
3| 4 5 6 7
4| 5 6 7 8
.
.
Count map values inc/dec linearly and with a max
limitation on the smallest die's max
ex. 2, 4 -> [1, 2, 2, 2, 1]
    3, 3 -> [1, 2, 3, 2, 1]
"""
def doubleDiceCall(n, m):
    countRet = [None]*(n+m-1)
    maxCount = min(m, n)

    # Symmetry allows for mirrored calculations
    for i in range(math.ceil(len(countRet)/2)):

        if i >= maxCount:
            countRet[i] = maxCount
            countRet[len(countRet)-1-i] = maxCount

        else:
            countRet[i] = i + 1
            countRet[len(countRet)-1-i] = i + 1
            
    return countRet


if __name__ == "__main__":
    # gui event start
    plt.ion()
    gameOn = True

    # Main dice collection variable
    dice = [[6, 6]]
    lines = []

    # Og figure
    fig, ax = plt.subplots()
    linetmp, = ax.plot([i for i in range(2, 13)], diceMap(dice[0]), marker='.')

    # TODO labels

    for _ in range(50):

        # TODO change values here

        # Redraw figure
        fig.canvas.draw()

        # flush gui events
        fig.canvas.flush_events()
        time.sleep(.1)