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
from bitarray import bitarray


class Solution:
    def __init__(self, data, modified=False, dev=False, do_strip=False, do_splitlines=True, split_char=None):
        if data and do_strip:
            data = data.strip()
        if data and do_splitlines:
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
        nums = "..."+self.data[0][0].split(": ")[1]+"..."
        added_left = added_right = 3 # count how many digits were added to the left
        print(added_left+added_right, nums)
        patterns = {}
        for p, flag in self.data[2:]:
            patterns[p] = flag
        print(patterns)

        print(f"{0:>2} {'.' * (5-added_left)}{nums}{'.' * (15-added_right)}")
        rounds = 200 if self.modified else 20
        for i in range(1,rounds+1):
            ptr = 0
            new_nums = nums[0:2]
            while ptr < len(nums)-4:
                window = nums[ptr:ptr+5]
                c = '.'
                if window in patterns:
                    c = patterns[window]
                new_nums += c
                ptr += 1
            new_nums += nums[-2:]
            to_add = 0
            if new_nums[2] == '#':
                new_nums = '.'+new_nums
                added_left += 1
            if new_nums[-3] == '#':
                new_nums += '.'
                added_right += 1
            nums = new_nums
            total = 0
            for j, c in enumerate(nums):
                if c == '#':
                    total += j - added_left
            print(f"{i:>2} {total:>5} {'.' * (5 - added_left)}{nums}{'.' * (15 - added_right)}")
        total = 0
        for i, c in enumerate(nums):
            if c == '#':
                total += i - added_left
        if self.modified:
            return (50000000000-rounds)*26 + total
        return total




    def second_part(self):
        return self.first_part()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = " => "
    DATA = None

    if not DATA:
        with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
            DATA = f.read()

    s = Solution(DATA, PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
    print(s.first_part() if not PART2 else s.second_part())
