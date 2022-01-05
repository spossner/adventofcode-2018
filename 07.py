import collections
import itertools
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

class Worker:
    def __init__(self, dev=False):
        self.dev = dev
        self.workload = None
        self.time = 0

    def finished(self):
        return self.workload is not None and self.time == 1

    def is_idle(self):
        return self.workload is None

    def start_work(self, workload):
        self.workload = workload
        self.time = 0 if workload is None else (ord(workload) - (64 if self.dev else 4))

    def work(self):
        if self.is_idle():
            return
        assert self.time > 1
        self.time -= 1

    def stop_work(self):
        assert self.time == 1
        workload = self.workload
        self.workload = None
        self.time = 0
        return workload

    def __str__(self):
        return f"{self.workload} ({self.time})" if self.workload is not None else '.'

    def __repr__(self):
        return self.__str__()


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
        self.dev = dev
        self.modified = modified

        self.dependencies = defaultdict(set)
        self.nodes = set()
        for row in self.data:
            name = row[7]
            depends_on = row[1]
            self.nodes.add(name)
            self.nodes.add(depends_on)
            self.dependencies[name].add(depends_on)

        self.queue = deque(sorted(self.nodes - self.dependencies.keys())) # pre fill nodes ready to proceed

    def first_part(self):
        dependencies = defaultdict(set)
        nodes = set()
        for row in self.data:
            id = row[7]
            depends_on = row[1]
            nodes.add(id)
            nodes.add(depends_on)
            dependencies[id].add(depends_on)

        d = deque(sorted(nodes-dependencies.keys()))
        result = ''
        seen = set()

        while d:
            id = d.popleft()
            if id in seen:
                continue
            seen.add(id)

            result += id

            for node in dependencies.keys():
                if node in seen:
                    continue
                dependencies[node] -= seen
                if not dependencies[node]:
                    bisect.insort(d, node)
        return result


    def second_part(self):
        result = ''
        workers = [Worker(self.dev) for _ in range(2 if self.dev else 5)]
        # for rounds in itertools.count():
        rounds = -1
        while True:
            if len(result) == len(self.nodes):
                break

            rounds += 1
            ready = set()
            for w in workers:
                if w.finished():
                    ready.add(w.stop_work())
                else:
                    w.work()
            if ready:
                result += ''.join(sorted(ready)) # append the ready
                pickup = set()
                for node in self.dependencies.keys():
                    self.dependencies[node] -= ready
                    if not self.dependencies[node]:
                        pickup.add(node)
                for node in pickup:
                    del self.dependencies[node]
                    bisect.insort(self.queue, node)

            for w in workers:
                if not self.queue:
                    break
                if w.is_idle():
                    node = self.queue.popleft() # next element to work on
                    w.start_work(node)

            print(rounds, workers, result)

        return rounds, result

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
        s = Solution(f.read(), PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.first_part() if not PART2 else s.second_part())