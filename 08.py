from __future__ import nested_scopes
import os
import sys
import math
import operator
import re
from collections import deque, defaultdict, namedtuple, Counter
from dataclasses import dataclass
from functools import total_ordering, reduce
from itertools import permutations, zip_longest, count
import bisect

import networkx as nx
import pygame as pg
import numpy as np
from aoc import Point, Rect, NORTH, rot_ccw, rot_cw, translate

class Node:
    def __init__(self):
        self.childs: [Node] = []
        self.meta: [int] = []

    def add_child(self, child):
        self.childs.append(child)

    def add_meta(self, meta: int):
        self.meta.append(meta)

    def get_meta_sum(self):
        ans = sum(self.meta)
        for c in self.childs:
            ans += c.get_meta_sum()
        return ans

    def get_sum(self):
        if self.childs:
            total = 0
            for idx in self.meta:
                if idx == 0 or idx > len(self.childs):
                    continue
                total += self.childs[idx-1].get_sum()
            return total
        else:
            return sum(self.meta)

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

    def parse_node(self, ptr=0):
        assert ptr < len(self.data)
        node = Node()
        child_count = self.data[ptr]
        meta_count = self.data[ptr+1]
        ptr += 2
        for _ in range(child_count):
            child, ptr = self.parse_node(ptr)
            node.add_child(child)
        for _ in range(meta_count):
            node.add_meta(self.data[ptr])
            ptr += 1
        return node, ptr

    def first_part(self):
        self.data = list(map(int, self.data))
        root, _ = self.parse_node()
        return root.get_sum() if self.modified else root.get_meta_sum()

    def second_part(self):
        return self.first_part()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = True
    SPLIT_LINES = False
    SPLIT_CHAR = ' '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.first_part() if not PART2 else s.second_part())
