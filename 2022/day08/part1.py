import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

ANS = 0

G=[]
V={}

up    = lambda x,y : (x + 1,y)
down  = lambda x,y : (x - 1,y)
left  = lambda x,y : (x,y - 1)
right = lambda x,y : (x,y + 1)

def lookaround(x,y, depth=-1,ox=0,oy=0,op=None):
	depth += 1
	if depth == 0:
		ox = x
		oy = y
		return lookaround(x,y,depth,ox,oy,up) \
				or lookaround(x,y,depth,ox,oy,down) \
				or	lookaround(x,y,depth,ox,oy,right) \
				or lookaround(x,y,depth,ox,oy,left)

	x,y = op(x,y)
#	print(depth)
	if not(0 <= x < MX) or not(0 <= y < MY):
		return True

	if G[x][y] >= G[ox][oy]:
		return False
	return lookaround(x,y,depth,ox,oy,op)


for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip('\n')
	G.append(L)

MX=len(G)
MY=len(G[0])
for I in range(0,len(G)):
	for J in range(0,len(G[I])):
		if lookaround(I,J):
			V[(I,J)]=1

ANS=len(V.keys())

# 1390 too low
print("ANSWER ==>  {}\n".format(ANS))
