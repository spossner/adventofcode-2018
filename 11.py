import os
import sys
import math
import operator
import re
from collections import deque, defaultdict, namedtuple, Counter
from functools import total_ordering, reduce
from itertools import permutations, zip_longest, count
import bisect

import networkx as nx
import pygame as pg
import numpy as np
from aoc import Point, Rect, NORTH, rot_ccw, rot_cw, translate


class Solution:
    def __init__(self, data, modified=False, dev=False, do_strip=False, do_splitlines=True, split_char=None):
        if data and do_strip and type(data) == str:
            data = data.strip()
        if data and do_splitlines and type(data) == str:
            data = data.splitlines()
        if data and split_char:
            if split_char == '':
                data = [list(row) for row in data] if do_splitlines else list(data)
            else:
                data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified
        self.dev = dev

    def first_part(self):
        # int((y * (x * x + 20 * x + 100) + s * (x + 10)) / 100) % 10
        w = h = 301
        s = self.data
        col_score = [[0] * w for _ in range(h)]
        grid = [[0] * w for _ in range(h)]
        serial_score = [s*(x+10) for x in range(w)]
        serial_score[0] = 0
        for x in range(1,w):
            col_score[1][x] = x*x + 20*x + 100
        for y in range(1, h):
            for x in range(1, w):
                col_score[y][x] = col_score[y-1][x] + col_score[1][x]
                grid[y][x] = int((col_score[y][x] + serial_score[x]) / 100) % 10 - 5
        # for row in grid[1:]:
        #     for v in row[1:]:
        #         print(f"{v:>3} ", end='')
        #     print()
        max_cells = None
        for size in range(1,w-1):
            for y in range(1,h-size-1):
                for x in range(1,w-size-1):
                    v = 0
                    for dy in range(size):
                        for dx in range(size):
                            v += grid[y+dy][x+dx]
                    if max_cells is None or v > max_cells[0]:
                        max_cells = (v, x, y, size)
                        print(f"\n{max_cells[1]},{max_cells[2]},{max_cells[3]} = {max_cells[0]}", end='.')
            print('.', end="")


    def second_part(self):
        return self.first_part()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = True
    PART2 = False
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = None
    DATA = 9810
    #DATA = 18
    #DATA = 42

    if not DATA:
        with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
            DATA = f.read()

    s = Solution(DATA, PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
    print(s.first_part() if not PART2 else s.second_part())
