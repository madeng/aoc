import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))

LX = len(LINES)
LY = len(LINES[0])
ANS = 0

V={}

up    = lambda x,y : (x + 1,y)
down  = lambda x,y : (x - 1,y)
left  = lambda x,y : (x,y - 1)
right = lambda x,y : (x,y + 1)

def lookaround(x,y, depth=-1,ox=0,oy=0,op=None,count=0):
	depth += 1
	if depth == 0:
		ox = x
		oy = y
		return lookaround(x,y,depth,ox,oy,up) \
				* lookaround(x,y,depth,ox,oy,down) \
				* lookaround(x,y,depth,ox,oy,right) \
				* lookaround(x,y,depth,ox,oy,left)

	x,y = op(x,y)
	if not(-1 < x < LX) or not(-1 < y < LY):
		return count
	count += 1
	if LINES[x][y] >= LINES[ox][oy]:
		return count
	return lookaround(x,y,depth,ox,oy,op, count)


for I in range(0,LX):
	for J in range(0,LY):
		V[(I,J)] = lookaround(I,J)

ANS=max(V.values())
print("ANSWER ==>  {}\n".format(ANS))
