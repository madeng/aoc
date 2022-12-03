import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

P1 = 0
P2 = 0

def prio(letter):
	val = ord(letter)
	lowerstart = 97
	upperstart = 65
	if val >= lowerstart:
		return val - lowerstart + 1
	return val - upperstart + 27

CH = []
for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip()
	# part 1
	HALF=int(len(L)/2)
	S1 = L[:HALF]
	S2 = L[HALF:]
	D = []
	[D.append(n) for n in S1 if n in S2 and n not in D]
	P1 += prio(D[0])

	# Part 2
	if I % 3 == 0:
		CH = [c for c in L]
		continue

	CH = [c for c in L if c in CH]
	if I % 3 == 2:
		P2 += prio(CH[0])

# 8018
print("1- part1 = {}".format(P1))
# 2518
print("2- part2 = {}".format(P2))
