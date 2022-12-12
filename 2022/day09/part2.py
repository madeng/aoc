import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))

S=(0,0)
K=[S]*10
V={}
V[S]=1

disty = lambda h,t:h[1]-t[1]
distx = lambda h,t:h[0]-t[0]

def movetail(i=1):
	if i >= len(K):
		return
	h=K[i-1]
	t=K[i]
	if istouching(h,t):
		return

	xdist=distx(h,t)
	ydist=disty(h,t)
	dx=0
	dy=0
	if abs(xdist) > 1 or abs(ydist) > 1:
		if xdist != 0:
			dx = 1 if xdist > 0 else -1
		if ydist != 0:
			dy = 1 if ydist > 0 else -1
	K[i]=(t[0]+dx,t[1]+dy)
	movetail(i+1)

def reg(t):
	V[t] = 1 if t not in V else V[t]+1

def istouching(h, t):
	val = True if abs(h[0]-t[0]) <= 1 and abs(h[1]-t[1]) <= 1 else False
#	print("checking if touching, h={}, t={}, val={}".format(h,t,val))
	return val


for L in LINES:
	D,N = [ int(s) if s.isdigit() else s for s in L.split(' ')]
	print(D,N)
	for S in range(N):
		H=K[0]
		if D=='R':
			K[0] = (H[0],H[1]+1)
		elif D=='L':
			K[0] = (H[0],H[1]-1)
		elif D=='U':
			K[0] = (H[0]-1,H[1])
		elif D=='D':
			K[0] = (H[0]+1,H[1])

		movetail()
		print(K)
		reg(K[-1])

ANS = len(V.keys())
# 2525 too low
# 2562
print("ANSWER ==>  {}\n".format(ANS))
