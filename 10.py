import os
import sys
import math
import operator
import re
from collections import deque, defaultdict, namedtuple, Counter
from functools import total_ordering, reduce
from itertools import permutations, zip_longest, count
import bisect

import aoc
import networkx as nx
import pygame as pg
import numpy as np
from aoc import Point, Rect, NORTH, rot_ccw, rot_cw, translate

SIZE = WIDTH, HEIGHT = 800, 600  # the width and height of our screen
BLOCK_SIZE = 5
BACKGROUND_COLOR = pg.Color('white')  # The background colod of our window
FPS = 60  # Frames per second


def dump_points(points):
    boundary = Rect.boundary(points).grow(3)
    row = None
    for p in boundary:
        if p.y != row:
            if row is not None:
                print()
            row = p.y
        print('#' if p in points else '.', end='')
    print()


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
        points = []
        bounds = [0, 0, 0, 0]
        for row in self.data:
            x, y, dx, dy = aoc.get_ints(row)
            bounds[0] = min(bounds[0], x)
            bounds[1] = min(bounds[1], y)
            bounds[2] = max(bounds[2], x)
            bounds[3] = max(bounds[3], y)
            points.append([Point(x, y), Point(dx, dy)])

        pg.init()
        screen = pg.display.set_mode(SIZE)
        clock = pg.time.Clock()

        boundary = Rect.boundary((bounds[0:2], bounds[2:]))
        step = 0
        paused = False
        direction = 1
        seconds = 0
        for i in count():
            for e in pg.event.get():
                if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_SPACE:
                        paused = not paused
                    elif e.key == pg.K_RIGHT:
                        step = 1
                        direction = 1
                    elif e.key == pg.K_LEFT:
                        step = 1
                        direction = -1

            clock.tick(FPS)
            BLOCK_SIZE = min(WIDTH / boundary.w, HEIGHT / boundary.h)
            if BLOCK_SIZE > 0.1:
                screen.fill(BACKGROUND_COLOR)
                for p, v in points:
                    pg.draw.rect(screen, pg.Color('blue'),
                                 (p.x * BLOCK_SIZE - (WIDTH>>1),p.y * BLOCK_SIZE-(HEIGHT>>1), BLOCK_SIZE, BLOCK_SIZE))
                pg.display.flip()

            if step != 0:
                paused = True
            elif paused:
                continue

            bounds = [0, 0, 0, 0]

            boost = max(1, int(min(boundary.w * 0.01, boundary.w * 0.01)))
            if boost < 10:
                boost = 1
            for p in points:
                p[0] = Point(p[0].x + direction * boost * p[1].x, p[0].y + direction * boost * p[1].y)
                bounds[0] = min(bounds[0], p[0].x)
                bounds[1] = min(bounds[1], p[0].y)
                bounds[2] = max(bounds[2], p[0].x)
                bounds[3] = max(bounds[3], p[0].y)
            new_boundary = Rect.boundary((bounds[0:2], bounds[2:]))
            if new_boundary.w > boundary.w or new_boundary.h > boundary.h:
                paused = True
            boundary = new_boundary
            seconds += direction * boost
            print(seconds, boost, direction, boundary)
            if step != 0:
                step -= 1

            # dump_points(set([p[0] for p in points]))

    def second_part(self):
        return self.first_part()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = None
    DATA = None

    if not DATA:
        with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
            DATA = f.read()

    s = Solution(DATA, PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
    print(s.first_part() if not PART2 else s.second_part())
