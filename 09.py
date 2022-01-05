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
from aoc.linked_list import ListNode


def dump_table(root, current):
    node = root
    while True:
        if node == current:
            print(f"({node.val})", end="")
        else:
            print(f" {node.val} ", end="")
        node = node.next_node
        if node == root:
            break
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
        players, marbles = aoc.get_ints(self.data)
        if self.modified:
            marbles *= 100
        print(players, marbles)
        root = node = ListNode(0)
        node.next_node = node
        node.prev_node = node

        scores = defaultdict(int)
        for round in range(1,marbles+1):
            if round % 23 == 0:
                current_player = round % players
                scores[current_player] += round
                for _ in range(7):
                    node = node.prev_node
                scores[current_player] += node.val
                node = node.next_node # got to next node (new current)...
                node.pop_prev() # ...and pop the previous node
            else:
                node = node.next_node.insert_after(round)
            if round % 10000 == 0:
                print(round)
                #dump_table(root, node)
        return max(scores.values())


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
    SPLIT_CHAR = None
    DATA = None

    # DATA = "9 players; last marble is worth 25 points"
    # DATA = "10 players; last marble is worth 1618 points"
    # DATA = "13 players; last marble is worth 7999 points"
    # DATA = "17 players; last marble is worth 1104 points"
    # DATA = "30 players; last marble is worth 5807 points"

    if not DATA:
        with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
            DATA = f.read()

    s = Solution(DATA, PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
    print(s.first_part() if not PART2 else s.second_part())
