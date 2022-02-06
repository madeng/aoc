import sys
import re

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

M = []
DX = 0
DY = 0
for I,LINE in enumerate(open(FILE)):
	DY = len(LINE.strip())
	DX = I + 1
	for J,C in enumerate(LINE.strip()):
		if C == '#':
			M.append((I,J))

T = 1
TREES = 0
MOV = [(1,3),(1,1),(1,5),(1,7),(2,1)]
for MOVX,MOVY in MOV:
	TREES = 0
	X,Y = 0,0
	while X < DX:
		if (X % DX, Y % DY) in M:
			TREES += 1
		X += MOVX
		Y += MOVY
	if (MOVX,MOVY) == (1,3):
		print("part1:", TREES)
	T *= TREES

print("part2:",T)
