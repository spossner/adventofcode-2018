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
    def __init__(self, data, modified=False, do_strip=False, do_splitlines=True, split_char=None):
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

    def solve(self):
        result = sys.maxsize
        for a in range(26):
            skip = (chr(a+65), chr(a+97))
            p = self.data
            i = 0
            while i < len(p) - 1:
                c = p[i]
                j = i + 1
                if self.modified and c in skip:
                    p = p[:i] + p[i + 1:]
                    continue
                if self.modified and p[j] in skip:
                    while j < len(p) and p[j] in skip:
                        j += 1
                    if j == len(p):
                        p = p[:i+1] # cut tail
                        break       # ..and finish
                d = p[j]
                if abs(ord(c) - ord(d)) == 32:
                    p = p[:i] + p[j + 1:] # cut from i to j (skipping characters to skip)
                    i = max(i - 1, 0)
                else:
                    i += 1
            result = min(result, len(p))
            if not self.modified:
                return result
        return result


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = True
    SPLIT_LINES = False
    SPLIT_CHAR = None

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
