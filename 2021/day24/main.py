from __future__ import annotations
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day24/input'

def read_input(a, b):
    global INPUT_INDEX,INPUT
    VAR[a] = INPUT[INPUT_INDEX]
    INPUT_INDEX += 1

def add(a, b):
    VAR[a] += b

def mul(a, b):
    VAR[a] *= b

def div(a, b):
    VAR[a] //= b

def modulo(a, b):
    VAR[a] %= b

def equal(a, b):
    VAR[a] = 1 if VAR[a] == VAR[b] else 0

INPUT_INDEX = 0
VAR = {'w','x','y','z'}
OP = {
    "in":read_input,
    "add":add,
    "mul":mul,
    "div":div,
    "mod":modulo,
    "eql":equal,
}
INPUT = "123"

for LINE in open(FILE):
    OP, COORD = LINE.strip().split(" ")

# print("part1: x = {}".format())

# print("part2: x = {}".format())