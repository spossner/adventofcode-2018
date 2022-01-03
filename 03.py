import os
import sys
import math
import operator
import re
from collections import deque, defaultdict, namedtuple, Counter
from functools import total_ordering, reduce
from itertools import permutations, zip_longest, count
import bisect

from aoc import Point, Rect, NORTH, rot_ccw, rot_cw, translate, get_ints
import networkx as nx
import pygame as pg
import numpy as np


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
        claims = []
        for row in self.data:
            id, x, y, w, h = get_ints(row)
            claims.append(Rect(x, y, w, h))  # ignore the ID - or if needed ID = idx+1
        overlap = set()
        overlaps = set(range(len(claims)))
        for a in range(len(claims) - 1):
            r1 = claims[a]
            for b in range(a + 1, len(claims)):
                r2 = claims[b]
                r_i = r1.intersection(r2)
                if r_i is None:
                    continue  # no intersection
                if a in overlaps:
                    overlaps.remove(a)

                if b in overlaps:
                    overlaps.remove(b)
                for p in r_i.points():
                    overlap.add(p)
        if self.modified:
            return set(map(lambda i:i+1, overlaps))
        return len(overlap)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = None

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
