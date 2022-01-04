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
from aoc import Point, Rect, NORTH, rot_ccw, rot_cw, translate, fetch


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
        self.data.sort(key=lambda e: e[0]+" "+e[1])
        current_guard = None
        asleep = None
        day = None
        ranges = {}
        for row in self.data:
            date, time, action, guard = fetch(row, 4)
            minute = int(time[-3:-1])
            date = date[1:]
            cmd = action[0]
            if cmd == 'G':
                current_guard = int(guard[1:])
                day = None
            elif cmd == 'f':
                if day is None:
                    day = date
                assert day == date
                asleep = minute
            elif cmd == 'w':
                assert asleep is not None
                assert day == date
                if current_guard not in ranges:
                    ranges[current_guard] = defaultdict(list)
                guard_ranges = ranges[current_guard]
                guard_ranges[day].append(range(asleep, minute))  # range(asleep, wakeup) - wakeup excl
                asleep = None

        print(ranges)
        max_minutes = None
        for id, guard_ranges in ranges.items():
            print(f"{id} had duty on {len(guard_ranges)} days")
            print(f"... and slept {sum(map(len,guard_ranges.values()))} times")
            time_asleep = sum([sum(map(len,ranges)) for ranges in guard_ranges.values()])
            print(f"... in total slept {time_asleep} minutes")
            if max_minutes is None or time_asleep > max_minutes[1]:
                max_minutes = (id, time_asleep)

        if self.modified:
            max_minutes = None
            for id, guard_ranges in ranges.items():
                counter = Counter()
                for day, protocol in guard_ranges.items():
                    for r in protocol:
                        counter.update(r)
                minute, times = counter.most_common(1)[0]
                if max_minutes is None or times > max_minutes[2]:
                    max_minutes = (id, minute, times)
            return max_minutes[0] * max_minutes[1]

        counter = Counter()
        print(ranges[max_minutes[0]])
        for day, protocol in ranges[max_minutes[0]].items():
            for r in protocol:
                counter.update(r)
        return counter.most_common(1)[0][0] * max_minutes[0]

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = ' '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())


    # 1313995 too high
    # 101262