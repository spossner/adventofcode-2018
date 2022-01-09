import functools
import os
import sys
from dataclasses import dataclass
from itertools import count

import aoc
from aoc import Point, Rect, rot_ccw, rot_cw, translate

DIRECTIONS = {
    '<': aoc.WEST,
    '>': aoc.EAST,
    '^': aoc.NORTH,
    'v': aoc.SOUTH,
}

TURNING = {
    '/': {
        aoc.NORTH: aoc.EAST,
        aoc.EAST: aoc.NORTH,
        aoc.WEST: aoc.SOUTH,
        aoc.SOUTH: aoc.WEST,
    },
    '\\': {
        aoc.NORTH: aoc.WEST,
        aoc.WEST: aoc.NORTH,
        aoc.EAST: aoc.SOUTH,
        aoc.SOUTH: aoc.EAST,
    }
}


@dataclass
class Car:
    direction: Point
    turns: int = 0
    moves: int = 0
    crashed: bool = False


class Solution:
    def __init__(self, data, modified=False, dev=False, do_strip=False, do_splitlines=True, split_char=None):
        if data and do_strip:
            data = data.strip()
        if data and do_splitlines:
            data = data.splitlines()
        if data and split_char is not None:
            if split_char == '':
                data = [list(row) for row in data] if do_splitlines else list(data)
            else:
                data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified
        self.dev = dev

    def parse_direction(self, c):
        return DIRECTIONS[c]

    def direction_str(self, direction):
        for k, v in DIRECTIONS.items():
            if v == direction:
                return k
        raise ValueError(f"unknwon direction {direction}")

    def dump_track(self, cars, crash=None):
        for y, row in enumerate(self.data):
            for x, v in enumerate(row):
                if cars and (x, y) in cars:
                    print(self.direction_str(cars[(x, y)].direction), end="")
                elif crash and crash == (x, y):
                    print('X', end="")
                else:
                    print(row[x], end="")
            print()

    def first_part(self):
        cars = {}
        for y, row in enumerate(self.data):
            for x, v in enumerate(row):
                if v in '<>^v':
                    cars[Point(x,y)] = Car(self.parse_direction(v))  # direction, moves so far
                    row[x] = '-' if v in '<>' else '|'  # fix the track

        self.dump_track(cars)
        for tick in count():
            car_positions = sorted(list(cars.keys()), key=functools.cmp_to_key(aoc.point_by_row))

            if tick == 490:
                print(f"check what is happening from here on.. ")
                self.dump_track(cars)
                print()

            new_cars = {}
            for pos in car_positions:
                car = cars[pos]
                if car.crashed:
                    continue # ignore crashed cars - they were removed instantly

                t = self.data[pos.y][pos.x]
                # do turning if needed
                if t in '/\\':
                    car.direction = TURNING[t][car.direction]
                elif t == '+':
                    indicator = car.turns % 3
                    if indicator == 0:
                        car.direction = rot_ccw(car.direction)
                    elif indicator == 2:
                        car.direction = rot_cw(car.direction)
                    car.turns += 1
                # move
                car.moves += 1
                new_pos = translate(pos, car.direction)

                # check collision - ignoring crashed cars
                if (new_pos in cars and not cars[new_pos].crashed) or (new_pos in new_cars and not new_cars[new_pos].crashed):
                    if new_pos in cars:
                        cars[new_pos].crashed = True
                    if new_pos in new_cars:
                        new_cars[new_pos].crashed = True

                    car.crashed = True
                    #self.dump_track(None, new_pos)
                    if not self.modified:
                        return (new_pos, car)
                else:
                    new_cars[new_pos] = car
            cars = {k:v for k,v in new_cars.items() if not v.crashed}
            if self.modified and len(cars) == 1:
                return cars.popitem()
            #self.dump_track(cars)
            #print()
        return None

    def second_part(self):
        return self.first_part()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True

    STRIP = False
    SPLIT_LINES = True
    SPLIT_CHAR = ''
    DATA = None

    if not DATA:
        if DEV:
            script += "-dev"
            if type(DEV) != bool:
                script += str(DEV)
        with open(f'{script}.txt') as f:
            DATA = f.read()

    s = Solution(DATA, PART2, DEV, STRIP, SPLIT_LINES, SPLIT_CHAR)
    print(s.first_part() if not PART2 else s.second_part())
