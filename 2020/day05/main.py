import sys
import re

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

def convert(txt):
	nb = 0
	ln = len(txt) - 1
	for i,c in enumerate(txt):
		if c == 'B' or c == 'R':
			nb += pow(2, ln - i)
	return nb


HASH=[]
for I,LINE in enumerate(open(FILE)):
	LINE = LINE.strip()
	ROW = convert(LINE[0:7])
	COL = convert(LINE[7:10])
	_h = ROW * 8 + COL
	HASH.append( _h)

print('part1:', max(HASH))

HASH.sort()
last = HASH[7]
for H in HASH[8:]:
	if last + 1 != H:
		print("part2:", H - 1)
		break
	last = H

