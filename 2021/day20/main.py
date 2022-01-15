import copy
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'tin'

def btoi(b: str) ->int:
    nb = 0
    for c in b:
        nb = (nb << 1) + int(c)
    return nb


def apply_r(x, y):
    global SIZE_X, SIZE_Y, INPUT, OUTPUT, R, DEFAULT_VALUE
    b = ''
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i < 0 or i >= SIZE_X or j < 0 or j >= SIZE_Y:
                b += DEFAULT_VALUE
                continue
            b += INPUT[i][j]
    OUTPUT[x][y] = R[btoi(b)]


def resize_input():
    global SIZE_X, SIZE_Y, INPUT
    INPUT.insert(0, [DEFAULT_VALUE for _ in range(SIZE_Y)])
    INPUT.append([DEFAULT_VALUE for _ in range(SIZE_Y)])
    for line in INPUT:
        line.insert(0, DEFAULT_VALUE)
        line.append(DEFAULT_VALUE)
    SIZE_X += 2
    SIZE_Y += 2


def print_array(darray):
    for line in darray:
        for c in line:
            print(c, end='')
        print()
    print("\n")

INPUT = []
for I, LINE in enumerate(open(FILE)):
    LINE = LINE.strip()
    if I == 0:
        R = []
        for C in LINE:
            TMP = '1' if C == '#' else '0'
            R.append(TMP)
    elif LINE.strip() == '':
        continue
    else:
        TMP = []
        for C in LINE:
            C = '1' if C == '#' else '0'
            TMP.append(C)
        INPUT.append(TMP)

SIZE_X = len(LINE)
SIZE_Y = len(INPUT)
DEFAULT_VALUE = '0'
# print(INPUT)
OUTPUT = INPUT
for LOOP_ID in range(1, 50 + 1):
    INPUT = OUTPUT
    resize_input()
    OUTPUT = copy.deepcopy(INPUT)
    for Y in range(len(INPUT)):
        for X in range(len(INPUT[Y])):
            apply_r(X, Y)
    DEFAULT_VALUE = R[0] if DEFAULT_VALUE == '0' else R[511]

    if LOOP_ID == 2 or LOOP_ID == 50:
        LIT_PX = 0
        for LINE in OUTPUT:
            for C in LINE:
                if C == '1':
                    LIT_PX += 1
        print("part1: lit_px = {}".format(LIT_PX))
