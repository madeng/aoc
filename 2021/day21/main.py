import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'tin'

class Player:
    start_pos = None
    pos = None
    points = 0

    def __init__(self, pos):
        self.start_pos = pos
        self.pos = pos

    def move(self, v):
        self.pos += v
        self.pos = self.pos % 10
        self.points += self.pos + 1

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
        ORIG_P1 = int(WORD[4])
    elif I == 1:
        ORIG_P2 = int(WORD[4])

P1 = Player(ORIG_P1)
P2 = Player(ORIG_P2)

DICE = DeterministicDice()
IS_P1_TURN = True
NBR_OF_ROLLS_AT_A_TIME = 3
while P1.points < 1000 and P2.points < 1000:
    VAL = DICE.roll(NBR_OF_ROLLS_AT_A_TIME)
    if IS_P1_TURN:
        P1.move(VAL)
    if not IS_P1_TURN:
        P2.move(VAL)
    IS_P1_TURN = not IS_P1_TURN

LOSER = P1 if P1.points < P2.points else P2
WINNER = P1 if P1.points > P2.points else P2
print(LOSER)
print(WINNER)
print("part1: {}".format(LOSER.points * DICE.nb_rolls))
