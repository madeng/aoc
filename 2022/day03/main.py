import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'input'

for I, DLINE in enumerate(open(FILE)):
	LINE = DLINE.strip().lower()


P1=0
P2=0
print("1- part1 = {}".format(P1))
print("2- part2 = {}".format(P2))
