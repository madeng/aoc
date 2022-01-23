from __future__ import annotations
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day25/input'


for LINE in open(FILE):
    OP, COORD = LINE.strip().split(" ")

# print("part1: x = {}".format())

# print("part2: x = {}".format())