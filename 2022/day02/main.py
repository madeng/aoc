import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

MAP={'x':'a','y':'b','z':'c'}
POINTS={'a':1,'b':2,'c':3 }
WIN={'a':'b','b':'c','c':'a'}
LOSE={'a':'c','b':'a','c':'b'}

def win(o,t):
	u = MAP[t]
	if o == u:
		return 3
	if WIN[o] == u:
		return 6
	return 0

def strat(o,t):
	if t == 'x':   return POINTS[LOSE[o]]
	elif t == 'y': return POINTS[o] + 3
	return POINTS[WIN[o]] + 6

S1=[]
S2=[]
for I, DLINE in enumerate(open(FILE)):
	LINE = DLINE.strip().lower()
	O,U = LINE.split(" ")
	S1.append(0)
	S1[I] = POINTS[MAP[U]]
	S1[I] += win(O,U)

	S2.append(0)
	S2[I] = strat(O,U)

#16936 too high
#15508 is right
P2=sum(S2)
# 13268 is right
P1=sum(S1)

print("1- part1 = {}".format(P1))

print("2- part2 = {}".format(P2))

