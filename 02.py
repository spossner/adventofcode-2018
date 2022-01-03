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

from aoc import Point, NORTH, rot_ccw, rot_cw, translate


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
        counts = [0] * 30
        for id in self.data:
            c = Counter(id)
            added = set()
            for v in c.values():
                if v in added:
                    continue
                added.add(v)
                counts[v] += 1
        if not self.modified:
            return counts[2]*counts[3]

        for id in self.data:
            for other in self.data:
                if id == other:
                    continue

                diffs = []
                for i in range(len(id)):
                    if id[i] != other[i]:
                        diffs.append(i)
                        if len(diffs) > 1:
                            break
                if len(diffs) > 1:
                    continue

                pos = diffs[0]
                return (id, other, pos, id[:pos]+id[pos+1:])



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = None

    with open(f'{script}{"-dev2" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
