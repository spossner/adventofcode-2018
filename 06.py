import os
import sys
import math
import operator
import re
from collections import deque, defaultdict, namedtuple, Counter
from functools import total_ordering, reduce
from itertools import permutations, zip_longest, count, chain
import bisect

import aoc
import networkx as nx
import pygame as pg
import numpy as np
from aoc import Point, Rect, NORTH, rot_ccw, rot_cw, translate

Marker = namedtuple('Marker', "id,p,count", defaults=['?', Point(), 0])

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
        points = []
        ids = set()
        for i, row in enumerate(self.data):
            x, y = aoc.get_ints(row)
            points.append(Marker(i,Point(x, y)))
            ids.add(i)

        if self.modified:
            return self.solve2(points, ids)

        grid = {}
        seen = defaultdict(set)

        d = deque(points)
        finite = None
        for i in range(10):
            finite = set(ids)
            for _ in range(len(d)):
                id, p, c = m = d.popleft()

                if p in seen[id]:
                    continue
                seen[id].add(p)
                if p in grid:
                    if grid[p].count == c:
                        grid[p] = Marker(None, p, c) # flag position as tied (with None-id in marker)
                else:
                    if id in finite:
                        finite.remove(id)
                    grid[p] = m
                for a in aoc.direct_adjacent_iter(p):
                    d.append(Marker(id, a, c+1))
            self.dump_grid(grid)
        print(len(finite), finite)
        c = defaultdict(int)
        result = 0
        for m in grid.values():
            if m.id in finite:
                c[m.id] += 1
                result = max(result, c[m.id])
        print(result, c)

    def solve2(self, points, ids, n=10000):
        boundary = Rect()
        marker = {}
        for m in points:
            boundary.extend(m.p.x, m.p.y)
            marker[m.p] = m.id
        scan = Rect(int(boundary.x - (n/len(points)))-1,int(boundary.y - (n/len(points)))-1,int(boundary.x+boundary.w+(n/len(points)))+1-min_x+1,int(boundary.y+boundary.h+(n/len(points)))+1-min_y+1)
        result = 0
        for p in scan.points():
            total = 0
            for c in points:
                total += aoc.manhattan_distance(p, c.p)
                if total >= n: # early stop of checking points
                    break
            if total < n: # check total sum of distances is less than given n
                result += 1 # found a candidate
        return result


    def dump_grid(self, grid):
        boundary = Rect.boundary(grid.keys()).grow(3)
        row = None
        for p in boundary.points():
            if p.y != row:
                if row is not None:
                    print()
                row = p.y
            if p in grid and grid[p].id is not None:
                print(grid[p].id if grid[p].count == 0 else grid[p].count, end="")
            else:
                print('.' if p not in grid else '.', end="")
        print("\n")


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = True
    PART2 = False
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = None

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
