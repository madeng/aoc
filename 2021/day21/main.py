import copy
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day21/tin'


class Player:
    pos = None
    points = None
    def __init__(self, pos, points=0):
        self.pos = pos
        self.points = points

    def move(self, v):
        self.pos = (v + self.pos) % 10
        self.points += self.pos + 1

    def copy(self):
        return Player(self.pos, self.points)

    def __str__(self):
        return "(start_at: {}, current_pos: {}, points: {})".format(self.start_pos, self.pos, self.points)

class DeterministicDice:
    value = 0
    nb_rolls = 0

    def roll(self, nb_times=1):
        self.nb_rolls += nb_times
        ret_val = 0
        for _ in range(nb_times):
            self.value += 1
            ret_val += self.value
        return ret_val

    def __str__(self):
        return "(DetDice: last value:{}, number of rolls: {})".format(self.value, self.nb_rolls)

INPUT = []
ORIG_P1 = None
ORIG_P2 = None
for I, LINE in enumerate(open(FILE)):
    LINE = LINE.strip()
    WORD = LINE.split(" ")
    if I == 0:
        ORIG_P1 = int(WORD[4]) - 1
    elif I == 1:
        ORIG_P2 = int(WORD[4]) - 1

P1 = Player(ORIG_P1)
P2 = Player(ORIG_P2)

DICE = DeterministicDice()
IS_P1_TURN = True
NBR_OF_ROLLS_AT_A_TIME = 3
while P1.points < 1000 and P2.points < 1000:
    DICE_RESULT = DICE.roll(NBR_OF_ROLLS_AT_A_TIME)
    if IS_P1_TURN:
        P1.move(DICE_RESULT)
    if not IS_P1_TURN:
        P2.move(DICE_RESULT)
    IS_P1_TURN = not IS_P1_TURN

LOSER = P1 if P1.points < P2.points else P2
WINNER = P1 if P1.points > P2.points else P2
print("part1: {}".format(LOSER.points * DICE.nb_rolls))


# Number of possibilities for each result of throwing a 3-sided dice 3 times
MIN_POSSIBLE_SUM = 3
MAX_POSSIBLE_SUM = 9

MAP_DICE_RESULT_2_POSSIBILITIES = {
    3:1,
    4:3,
    5:6,
    6:7,
    7:6,
    8:3,
    9:1,
}
# Return a tuple
def move(p: tuple, val: int):
    # p[0]: position, p[1]: points
    pos = (val + p[0]) % 10
    return pos, p[1] + pos

WINNING_POINTS = 15
def play(p1:tuple, p2:tuple, is_p1_turn=True, nb_universe=1):
    if p1[1] >= WINNING_POINTS:
        return nb_universe, 0
    if p2[1] >= WINNING_POINTS:
        return 0, nb_universe
    w1 = 0
    w2 = 0
    possible = [(p1, p2, is_p1_turn, nb_universe)]
    while len(possible) > 0:
        p1, p2, is_p1_turn, nb_universe = possible.pop()
        if p1[1] >= WINNING_POINTS:
            w1 += nb_universe
            continue
        if p2[1] >= WINNING_POINTS:
            w2 += nb_universe
            continue
        for dice_result in range(MIN_POSSIBLE_SUM, MAX_POSSIBLE_SUM + 1):
            if is_p1_turn:
                new_p1 = move(p1, dice_result)
                new_p2 = p2
            else:
                new_p1 = p1
                new_p2 = move(p2, dice_result)
            possible.append((new_p1, new_p2, not is_p1_turn, nb_universe * MAP_DICE_RESULT_2_POSSIBILITIES[dice_result]))

    return w1, w2


SUM_WINNING_P1, SUM_WINNING_P2 = play((0,0), (0,0))
print("part2: p1: {}, p2: {}".format(SUM_WINNING_P1, SUM_WINNING_P2))
