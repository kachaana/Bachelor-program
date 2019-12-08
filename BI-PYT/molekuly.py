#!/usr/bin/env python3

"""
Zahrejte si na molekulu: Vystartujte z náhodného místa konzole náhodným směrem a na okrajích konzole se odrážejte podle (ideálního) zákona odrazu.

Řešte výše uvedenou úlohu z „Hrátek s printem“, tedy Pohyb molekuly v krabici, s následujícími zesložitěními:

 * vykreslete okraje „krabice“ (tedy terminálu) a pohybujte se pouze mezi nimi;
 * náraz molekuly do stěny vhodně zvýrazněte;
 * nechte krabicí létat přinejmenším dvě molekuly, přičemž řešte i jejich vzájemnou srážku.
 * Molekuly se mohou pohybovat všemi směry, tedy i diagonálně.
"""


import os
import random
from enum import Enum
import time


COLUMNS, ROWS = os.get_terminal_size()
matrix = [[0 for x in range(COLUMNS)] for y in range(ROWS + 1)]
COUNT_ITEMS = 10
list_items = []


RED = '\033[31;1m'
WHITE = '\033[37;1m'
PINK = '\033[35;1m'
GREEN = '\033[32;1m'


# Printing borders

def print_box():
    print('\033[?25l')
    for i in range(1, ROWS, 1):
        for j in range(1, COLUMNS, 1):
            if i == 1 or i == ROWS - 1 or j == 1 or j == COLUMNS - 1 or j == COLUMNS - 2 or j == 2:
                print('\033[' + str(i) + ';' + str(j) + 'H\033[44m' + ' ', end='')
            else:
                print('\033[' + str(i) + ';' + str(j) + 'H\033[40m' + ' ', end='')
    print('\033[' + str(ROWS) + ';' + str(0) + 'H\033[0m', end='')


class Directions(Enum):
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    UP_LEFT = 3
    DOWN_RIGHT = -3
    UP_RIGHT = 4
    DOWN_LEFT = -4


class Item:
    def __init__(self, x, y, d, i, m):
        self.x = x
        self.y = y
        self.d = d
        self.i = i
        self.m = m


def set_first_coords():
    x = random.randint(3, ROWS - 3)
    y = random.randint(3, COLUMNS - 3)
    d = random.choice(list(Directions))
    return x, y, d


list_walls = [1, 8, 3, 6, 4, 7, 5, 9]

"""
188888883
9       6
9       6
9       6
577777774
"""


# Initialization of matrix of items

def matrix_init():
    for i in range(0, ROWS + 1, 1):
        for j in range(0, COLUMNS, 1):
            if i == 0 or i == 1:
                matrix[i][j] = 8
            if i == ROWS - 1 or i == ROWS:
                matrix[i][j] = 7
            if j == 0 or j == 1 or j == 2:
                matrix[i][j] = 9
            if j == COLUMNS - 1 or j == COLUMNS - 2:
                matrix[i][j] = 6
            if (i == 0 or i == 1) and (j == 0 or j == 1):
                matrix[i][j] = 1
            if (i == 0 or i == 1) and j == COLUMNS - 1:
                matrix[i][j] = 3
            if i == ROWS - 1 and j == COLUMNS - 1:
                matrix[i][j] = 4
            if i == ROWS - 1 and (j == 0 or j == 1):
                matrix[i][j] = 5


# Getting new coordinates according to the direction

def new_coords(x, y, dir):
    if dir == Directions.UP:
        return x - 1, y, dir
    if dir == Directions.UP_RIGHT:
        return x - 1, y + 1, dir
    if dir == Directions.UP_LEFT:
        return x - 1, y - 1, dir
    if dir == Directions.DOWN:
        return x + 1, y, dir
    if dir == Directions.DOWN_RIGHT:
        return x + 1, y + 1, dir
    if dir == Directions.DOWN_LEFT:
        return x + 1, y - 1, dir
    if dir == Directions.LEFT:
        return x, y - 1, dir
    if dir == Directions.RIGHT:
        return x, y + 1, dir


# Swap directions

def swap(attacker, suffered):
    tmp = attacker.d
    attacker.d = suffered.d
    suffered.d = tmp


def change_direction_wall(item, wall):
    if wall == 1:
        item.d = Directions.DOWN_RIGHT
        return
    if wall == 3:
        item.d = Directions.DOWN_LEFT
        return
    if wall == 4:
        item.d = Directions.UP_LEFT
        return
    if wall == 5:
        item.d = Directions.UP_RIGHT
        return
    if item.d == Directions.UP and wall == 8:
        item.d = Directions.DOWN
        return
    if item.d == Directions.DOWN and wall == 7:
        item.d = Directions.UP
        return
    if item.d == Directions.LEFT and wall == 9:
        item.d = Directions.RIGHT
        return
    if item.d == Directions.RIGHT and wall == 6:
        item.d = Directions.LEFT
        return
    if wall == 8:
        if item.d == Directions.UP_RIGHT:
            item.d = Directions.DOWN_RIGHT
            return
        elif item.d == Directions.UP_LEFT:
            item.d = Directions.DOWN_LEFT
            return
    elif wall == 6:
        if item.d == Directions.DOWN_RIGHT:
            item.d = Directions.DOWN_LEFT
            return
        elif item.d == Directions.UP_RIGHT:
            item.d = Directions.UP_LEFT
            return
    elif wall == 7:
        if item.d == Directions.DOWN_RIGHT:
            item.d = Directions.UP_RIGHT
            return
        elif item.d == Directions.DOWN_LEFT:
            item.d = Directions.UP_LEFT
            return
    elif wall == 9:
        if item.d == Directions.UP_LEFT:
            item.d = Directions.UP_RIGHT
            return
        elif item.d == Directions.DOWN_LEFT:
            item.d = Directions.DOWN_RIGHT
            return


def attacker_up(attacker, suffered):
    if suffered.d == Directions.RIGHT:
        suffered.d = Directions.UP_RIGHT
        attacker.d = Directions.UP_LEFT
        return
    elif suffered.d == Directions.LEFT:
        suffered.d = Directions.UP_LEFT
        attacker.d = Directions.UP_RIGHT
        return
    elif suffered.d == Directions.DOWN_LEFT:
        suffered.d = Directions.UP_LEFT
        attacker.d = Directions.RIGHT
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        suffered.d = Directions.UP_RIGHT
        attacker.d = Directions.LEFT
        return
    elif suffered.d == Directions.UP_RIGHT or suffered.d == Directions.UP_LEFT:
        attacker.d = suffered.d
        suffered.d = Directions.UP
        return


def attacker_down(attacker, suffered):
    if suffered.d == Directions.RIGHT:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.DOWN_LEFT
        return
    elif suffered.d == Directions.LEFT:
        suffered.d = Directions.DOWN_LEFT
        attacker.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.DOWN_LEFT:
        suffered.d = Directions.LEFT
        attacker.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        suffered.d = Directions.RIGHT
        attacker.d = Directions.DOWN_LEFT
        return
    elif suffered.d == Directions.UP_LEFT:
        attacker.d = Directions.LEFT
        suffered.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.UP_RIGHT:
        attacker.d = Directions.RIGHT
        suffered.d = Directions.DOWN_LEFT
        return


def attacker_left(attacker, suffered):
    if suffered.d == Directions.UP:
        suffered.d = Directions.UP_LEFT
        attacker.d = Directions.DOWN_LEFT
        return
    elif suffered.d == Directions.DOWN:
        suffered.d = Directions.DOWN_LEFT
        attacker.d = Directions.UP_LEFT
        return
    elif suffered.d == Directions.UP_RIGHT:
        suffered.d = Directions.UP
        attacker.d = Directions.UP_LEFT
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        suffered.d = Directions.DOWN
        attacker.d = Directions.DOWN_LEFT
        return
    elif suffered.d == Directions.UP_LEFT:
        suffered.d = Directions.LEFT
        attacker.d = Directions.UP_LEFT
        return
    elif suffered.d == Directions.DOWN_LEFT:
        suffered.d = Directions.LEFT
        attacker.d = Directions.DOWN_LEFT
        return


def attacker_right(attacker, suffered):
    if suffered.d == Directions.UP:
        suffered.d = Directions.UP_RIGHT
        attacker.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.DOWN:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.UP_RIGHT
        return
    elif suffered.d == Directions.UP_RIGHT:
        suffered.d = Directions.RIGHT
        attacker.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        suffered.d = Directions.RIGHT
        attacker.d = Directions.UP_RIGHT
        return
    elif suffered.d == Directions.UP_LEFT:
        suffered.d = Directions.UP
        attacker.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.DOWN_LEFT:
        suffered.d = Directions.DOWN
        attacker.d = Directions.UP_RIGHT
        return


def attacker_down_left(attacker, suffered):
    if suffered.d == Directions.UP:
        suffered.d = Directions.UP_LEFT
        attacker.d = Directions.LEFT
        return
    elif suffered.d == Directions.DOWN:
        suffered.d = Directions.DOWN_LEFT
        attacker.d = Directions.LEFT
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        suffered.d = Directions.DOWN_LEFT
        attacker.d = Directions.DOWN_RIGHT
        return
    elif suffered.d == Directions.LEFT:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.UP_LEFT
        return
    elif suffered.d == Directions.RIGHT:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        swap(attacker, suffered)
        return


def attacker_down_right(attacker, suffered):
    if suffered.d == Directions.UP:
        suffered.d = Directions.UP_RIGHT
        attacker.d = Directions.RIGHT
        return
    elif suffered.d == Directions.DOWN:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.RIGHT
        return
    elif suffered.d == Directions.UP_RIGHT:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.UP_RIGHT
        return
    elif suffered.d == Directions.LEFT:
        suffered.d = Directions.DOWN_LEFT
        attacker.d = Directions.RIGHT
        return
    elif suffered.d == Directions.RIGHT:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.DOWN_LEFT:
        swap(attacker, suffered)
        return


def attacker_up_right(attacker, suffered):
    if suffered.d == Directions.UP:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.DOWN:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.UP
        return
    elif suffered.d == Directions.LEFT:
        suffered.d = Directions.UP_LEFT
        attacker.d = Directions.RIGHT
        return
    elif suffered.d == Directions.RIGHT:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.UP_LEFT:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.DOWN_RIGHT:
        swap(attacker, suffered)
        return


def attacker_up_left(attacker, suffered):
    if suffered.d == Directions.UP:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.DOWN:
        suffered.d = Directions.DOWN_LEFT
        attacker.d = Directions.UP_RIGHT
        return
    elif suffered.d == Directions.LEFT:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.RIGHT:
        suffered.d = Directions.DOWN_RIGHT
        attacker.d = Directions.UP
        return
    elif suffered.d == Directions.UP_RIGHT:
        swap(attacker, suffered)
        return
    elif suffered.d == Directions.DOWN_LEFT:
        swap(attacker, suffered)
        return


def items_collapse(attacker, suffered):
    dir_a = attacker.d
    dir_s = suffered.d
    suffered.c = PINK
    if dir_a.value == (- dir_s.value):
        attacker.d = suffered.d
        suffered.d = dir_a
    if attacker.d == Directions.UP:
        attacker_up(attacker, suffered)
        return
    if attacker.d == Directions.DOWN:
        attacker_down(attacker, suffered)
        return
    if attacker.d == Directions.LEFT:
        attacker_left(attacker, suffered)
        return
    if attacker.d == Directions.RIGHT:
        attacker_right(attacker, suffered)
        return
    if attacker.d == Directions.DOWN_LEFT:
        attacker_down_left(attacker, suffered)
        return
    if attacker.d == Directions.DOWN_RIGHT:
        attacker_down_right(attacker, suffered)
        return
        return
    if attacker.d == Directions.UP_RIGHT:
        attacker_up_left(attacker, suffered)
        return
    if attacker.d == Directions.UP_LEFT:
        attacker_up_right(attacker, suffered)
        return


def run_items(item):
    print('\033[0;0H', end='')
    print(WHITE)
    print('\033[' + str(item.x) + ';' + str(item.y) + 'H\033[40m' + 'o', end='\r')
    time.sleep(0.01)
    print('\033[' + str(item.x) + ';' + str(item.y) + 'H\033[40m' + ' ', end='')
    x2, y2, d = new_coords(item.x, item.y, item.d)
    matrix[item.x][item.y] = 0
    if matrix[x2][y2] in list_walls:
        change_direction_wall(item, matrix[x2][y2])
        x2 = item.x
        y2 = item.y
        print(RED)
    if isinstance(matrix[x2][y2], list):
        tmp = matrix[x2][y2]
        item_suff = list_items[tmp[1]]
        items_collapse(item, item_suff)
        print(PINK)
        print('\033[' + str(item.x) + ';' + str(item.y) + 'H' + '\033[40m' + 'o', end='\r')
        time.sleep(0.007)
        print('\033[' + str(item.x) + ';' + str(item.y) + 'H\033[40m' + ' ', end='')
        x2, y2, d = new_coords(item.x, item.y, item.d)
    else:
        print('\033[' + str(x2) + ';' + str(y2) + 'H\033[40m' + 'o', end='\r')
        item.x = x2
        item.y = y2
        matrix[x2][y2] = [2, item.i]
    print('\033[' + str(ROWS) + ';' + str(0) + 'H', end='')


def items_init():
    for i in range(COUNT_ITEMS):
        x, y, d = set_first_coords()
        matrix[x][y] = [2, i]
        tmp = Item(x, y, d, i, 0)
        list_items.append(tmp)
    while 1:
        for j in list_items:
            if j.m == 0:
                run_items(j)


def initialization_function():
    print_box()
    matrix_init()
    items_init()


if __name__ == "__main__":
    try:
        initialization_function()
    except KeyboardInterrupt:
        print('\033[' + str(ROWS) + ';' + str(0) + 'H' + 'THE END')

