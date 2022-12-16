import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
ANS = 0

def present(grid):
	print('\n'.join([''.join([\
			'.' if grid[x][y] == 0 \
			else '#' if grid[x][y] == 1 \
			else 'o' if grid[x][y] == 2 \
			else '+' \
			for y in range(len(grid[0]))]) \
			for x in range(len(grid))]) \
	)

# Return true if the sand stopped somewhere, false if it falls outside the cave.
def drop_sand(x,y):
	ox,oy = (x,y)
	while True:
		hole_found = False
		for dx,dy in zip([1,1,1],[0,-1,1]):
			if GRID[x+dx][y+dy] != 0:
				continue
			x += dx
			y += dy
			hole_found = True
			break
		if not hole_found:
#			print('position found ({},{})'.format(x,y))
			GRID[x][y] = 2
			break
	if (x,y) == (ox,oy):
		return False
	return True


ALL_COORDS = []
leftmost = 100000
rightmost = 0
bottom = 0
for line in LINES:
	coords = [list(map(int, s.split(','))) for s in line.split(' -> ')]
	leftmost = min([c[0] for c in coords] + [leftmost])
	rightmost = max([c[0] for c in coords] + [rightmost])
	bottom = max([c[1] for c in coords] + [bottom])
	ALL_COORDS.append(coords)

LX = bottom + 1 +2
leftmost = min(leftmost, 500 - LX - 2)
rightmost = max(rightmost, 500 + LX + 2)
LY = rightmost - leftmost + 1

# Source of sand (x,y)
SX = 0
SY = 500 - leftmost

# Create the additional line at the very bottom
BOTTOM_LINE = [[rightmost, LX - 1],[leftmost, LX - 1]]
ALL_COORDS.append(BOTTOM_LINE)
GRID = [[0]*LY for _ in range(LX)]
GRID[SX][SY] = 3
for coords in ALL_COORDS:
	for c1,c2 in zip(coords[:-1],coords[1:]):
		left = min(c1[0],c2[0]) - leftmost
		right = max(c1[0],c2[0]) + 1 - leftmost
		for y in range(left,right):
			up = min(c1[1],c2[1])
			down = max(c1[1],c2[1]) + 1
			for x in range(up,down):
				GRID[x][y] = 1

count = 0
while drop_sand(SX,SY):
	count += 1

ANS=count + 1
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
