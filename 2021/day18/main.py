import sys
import re
from dataclasses import dataclass

infile = sys.argv[1] if len(sys.argv)>1 else 'testinput'

class Snailfish:
    parent = None
    x = None
    y = None

    def __init__(self, parent, x, y):
        self.x = x
        self.y = y

    def find_action(self, level=0) -> tuple:
        if type(self.x) is not Snailfish and type(self.y) is not Snailfish \
                and level >= 3:
            return ("explode", self)

        for child in [self.x, self.y]:
            if type(child) is Snailfish:
                action, p = child.find_action(level + 1)
                if action is not None:
                    return (action, p)
            else:
                if child > 9:
                    return ("split", self)

        return (None, None)

    def __str__(self):
        return "({},{})".format(self.x, self.y)


def parse_line(s) -> Snailfish:
    def build_snail(ancestor=None) -> Snailfish:
        nonlocal offset, s
        assert len(s) >= 5
        assert s[offset] == "["

        ignored_chars = r"[,\]]"
        state = 0
        offset += 1
        cur_snail = Snailfish(ancestor, None, None)
        while offset < len(s):
            c = s[offset]
            if re.match(ignored_chars, c):
                offset += 1
                continue

            if re.match(r"[0-9]", c):
                val = int(c)
                offset += 1
            elif c == "[":
                val = build_snail(cur_snail)
            else:
                print("Unexpected char at {}: {}".format(offset, c))
                return None

            if state == 0:
                cur_snail.x = val
                state += 1
            elif state == 1:
                cur_snail.y = val
                return cur_snail
            else:
                print("invalid state!")
                return None
    offset = 0
    return build_snail()


def explode_snail(s):
    pass


def split_snail(s):
    pass


ACTIONS = {
    "explode": explode_snail,
    "split": split_snail,
}

for line in open(infile):
    line = line.strip()
    print(line)
    MAIN = parse_line(line)
    print(MAIN)

    ACTION,SNAIL = MAIN.find_action()
    while ACTION is not None:
        if ACTION not in ACTIONS:
            print("unknown action:", ACTION)
            break
        ACTIONS[ACTION](SNAIL)
        break

