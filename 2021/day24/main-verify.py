import sys
import numpy as np

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day24/input'

if FILE == 'day24/input-simplified':
    INIT_VAR = {
        'w':0,
        'x':0,  # Simplified value
        'y':26, # Simplified value
        'z':np.arange(15,24,dtype=int), # Simplified to the values of z after the first round
    }
else:
    # Non-simplified version
    INIT_VAR = {
        'w':0,
        'x':0,
        'y':0,
        'z':0,
    }
VAR = INIT_VAR

INPUT_NBR = 0
INPUT = "0"*14 # Enter a number to verify
def read_input(a, b=0):
    global INPUT_NBR
    assert INPUT_NBR < len(INPUT)
    VAR[a] = int(INPUT[INPUT_NBR])
    # if INPUT_NBR % 2 == 0:
    #     VAR[a] = np.arange(1,10)
    # else:
    #     VAR[a] = np.arange(9, 0, -1)
    print("INPUT round {}".format(INPUT_NBR))
    print_reg()
    INPUT_NBR += 1

def get_val(val):
    if val in VAR.keys():
        c = VAR[val]
        if isinstance(c, np.ndarray) and (c == c[0]).all():
            c = c[0]
            VAR[val] = c
    else:
        c = int(val)
    return c

def add(a, b):
    assert a is not None and b is not None
    # assert isinstance(VAR[a], np.ndarray)
    val = get_val(b)
    VAR[a] = VAR[a] + val

def mul(a, b):
    assert a is not None and b is not None
    val = get_val(b)
    VAR[a] = VAR[a] * val

def div(a, b):
    assert a is not None and b is not None
    val = get_val(b)
    assert val != 0
    VAR[a] = VAR[a] // val

def modulo(a, b):
    assert a is not None and b is not None
    # assert type(VAR[a]) == np.ndarray
    val = get_val(b)
    VAR[a] = VAR[a] % val

def equal(a, b):
    assert a is not None and b is not None
    # assert type(VAR[a]) == np.ndarray
    val = get_val(b)
    VAR[a] = 1 * np.equal(VAR[a],val)

def print_reg():
    global VAR
    for key, val in VAR.items():
        print("part1: {} = {}".format(key, val))

OP = {
    "inp":read_input,
    "add":add,
    "mul":mul,
    "div":div,
    "mod":modulo,
    "eql":equal,
}
if __name__ == '__main__':
    for LINE in open(FILE):
        OP_STR, COORD = LINE.strip().split(" ",1)
        assert OP_STR in OP.keys()
        PARAMS = COORD.split(" ")
        # print("\n{} {}".format(OP_STR, PARAMS))
        OP[OP_STR](*PARAMS)
        print_reg()

    print("\nEND RESULTS")
    print_reg()
    # print("part1: x = {}".format(VAR))
    #
