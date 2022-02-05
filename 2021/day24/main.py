import sys
import os

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day24/input'

INIT_VAR = {
    'w':0,
    'x':0,
    'y':0,
    'z':0,
}

class RangeList:
    def __init__(self, *range_list):
        self.range_list = []
        for r in range_list:
            assert isinstance(r, Range)
            self.range_list.append(r)

    def __repr__(self):
        return str(self.range_list)

    def __add__(self, other):
        if isinstance(other, int):
            num = other
            for r in self.range_list:
                r = r + other
        elif isinstance(other, Range):
            self.range_list.append(other)
        else:
            assert False
        return self

    def __mul__(self, other):
        assert isinstance(other, int)
        if other == 0:
            return 0
        tmp_list = []
        for r in self.range_list:
            tmp_list.append(r * other)
        self.range_list = tmp_list
        return self

    def __floordiv__(self, other):
        assert isinstance(other, int)
        tmp_list = []
        for r in self.range_list:
            result = r // other
            if result == 0:
                continue
            tmp_list.append(result)
        if len(tmp_list) == 1:
            return tmp_list[0]
        self.range_list = tmp_list
        return self

    def __mod__(self, other):
        tmp_list = []
        for r in self.range_list:
            result = r % other
            if result == 0:
                continue
            tmp_list.append(result)
        if len(tmp_list) == 1:
            return tmp_list[0]
        self.range_list = tmp_list
        return self

class Range:
    def __init__(self, name, start=1, length=9, step_size=1):
        self.name = name
        self.start = start
        self.length = length
        self.step_size = step_size

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        ret = ''
        if self.step_size == 1:
            ret += "W{}[{},{}]".format(self.name, self.start, self.start + self.length - 1)
        else:
            ret += "{} * (W{}[{},{}])".format(
                self.step_size, self.name, self.start, self.start + (self.length - 1) * self.step_size)
        return ret

    def __copy__(self):
        return Range(self.name, self.start, self.length, self.step_size)

    def __add__(self, nb):
        if isinstance(nb, int):
            r = self.__copy__()
            r.start += nb
        else:
            r = RangeList(self, nb)
        return r

    def __mul__(self, nb):
        assert isinstance(nb, int)
        if nb == 0:
            return 0
        r = self.__copy__()
        r.start *= nb
        r.step_size *= nb
        return r

    def __mod__(self, nb):
        if self.step_size % 26 == 0:
            return 0
        assert self.start + self.length - 1 < nb
        r = self.__copy__()
        r.step_size %= nb
        r.start %= nb
        if r.step_size == 0:
            return 0
        return r

    def __floordiv__(self, nb):
        assert isinstance(nb, int)
        assert self.start + self.length - 1 < 26 or self.step_size >= 26
        r = self.__copy__()
        r.start //= nb
        r.step_size //= nb
        if r.start == 0 and r.step_size == 0:
            return 0
        return r

    def equal(self, r2):
        if isinstance(r2, int):
            r2 = Range('int:{}'.format(r2), r2, length=1)
        assert isinstance(r2, Range)
        r1 = self
        assert r1.step_size == 1
        assert r2.step_size == 1
        if r1.start > r2.start + r2.length - 1 or r1.start + r1.length - 1 < r2.start:
            return 0, None
        assert r1.length == r2.length
        if r1.start == r2.start:
            return 1, None
        elif r1.start < r2.start:
            tmp = r1
            r1 = r2
            r2 = tmp
        # Range2.start is < Range1.start
        overlap_size = r2.start + r2.length - r1.start
        # Overlapping part
        n_start1 = 1
        n_start2 = r1.start - r2.start + 1
        # non-overlapping part
        no_start1 = n_start1 + overlap_size
        no_start2 = 1
        return 1, [
            [Range(r1.name, n_start1, overlap_size),
             Range(r2.name, n_start2, overlap_size)],
            [Range(r1.name, no_start1, r1.length - overlap_size),
             Range(r2.name, no_start2, r2.length - overlap_size)]
        ]


INPUT_NBR = 0
def read_input(a, b=0):
    global INPUT_NBR
    assert INPUT_NBR < 14
    VAR[a] = Range("{}".format(INPUT_NBR))
    # print("INPUT round {}".format(INPUT_NBR))
    INPUT_NBR += 1

def get_val(val):
    if val in VAR.keys():
        c = VAR[val]
    else:
        c = int(val)
    return c

def add(a, b):
    assert a is not None and b is not None
    val = get_val(b)
    if isinstance(val, RangeList):
        VAR[a] = val + VAR[a]
    elif isinstance(VAR[a], RangeList):
        VAR[a] = VAR[a] + val
    elif isinstance(val, Range):
        VAR[a] = val + VAR[a]
    else:
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

def mod(a, b):
    assert a is not None and b is not None
    val = get_val(b)
    VAR[a] = VAR[a] % val

COND_LIST = []
FORK_LIST = []
def equal(a, b):
    assert a is not None and b is not None
    assert not isinstance(a, RangeList) and not isinstance(b, RangeList)
    val1 = VAR[a]
    val2 = get_val(b)
    if isinstance(val2, Range):
        result = val2.equal(val1)
    elif isinstance(val1, Range):
        result = val1.equal(val2)
    else:
        result = (1 if val1 == val2 else 0, None)
    if result[1] is None:
        VAR[a] = result[0]
        return
    # There is a condition for it to be True or False
    global COND_LIST, FORK_LIST
    child = os.fork()
    if child != 0:
        COND_LIST.append(result[1][0])
        VAR[a] = 1
    else:
        COND_LIST.append(result[1][1])
        VAR[a] = 0
    FORK_LIST.append(child)

OP = {
    "inp":read_input,
    "add":add,
    "mul":mul,
    "div":div,
    "mod":mod,
    "eql":equal,
}

VAR = INIT_VAR
for LINE_NO,LINE in enumerate(open(FILE)):
    LINE = LINE.strip()
    OP_STR, COORD = LINE.split(" ",1)
    assert OP_STR in OP.keys()
    PARAMS = COORD.split(" ")
    OP[OP_STR](*PARAMS)

if VAR['z'] == 0:
    print("condition list=",COND_LIST)
# print("part1: x = {}".format(VAR))
