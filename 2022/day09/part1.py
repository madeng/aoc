import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))

H=(0,0)
T=(0,0)
V={}
V[T]=1

up   = lambda x,y,n:(x+n,y)
down = lambda x,y,n:(x-n,y)
left = lambda x,y,n:(x,y-n)
right= lambda x,y,n:(x,y+n)

dist = lambda x,y,a,b:abs(x-a)+abs(y-b)
disty = lambda x,y,a,b:abs(y-b)
distx = lambda x,y,a,b:abs(x-a)

def reg(t):
	V[t] = 1 if t not in V else V[t]+1

#def movetail(h,t):
#	if istouching(h,t):
#		return
#	if dist(h,t) > 2:
#		if distx(h,t) > 1:
#			return

def istouching(h, t):
	return True if abs(h[0]-t[0]) <= 1 and abs(h[1]-t[1]) <= 1 else False


for L in LINES:
	D,N = [ int(s) if s.isdigit() else s for s in L.split(' ')]
	print(D,N)
	for S in range(N):
		if D=='R':
			H = (H[0],H[1]+1)
			if istouching(H,T):
				continue
			T = (H[0],T[1]+1)
			print('moved tail:{},head={}'.format(T, H))
			reg(T)
		elif D=='L':
			H = (H[0],H[1]-1)
			if istouching(H,T):
				continue
			T = (H[0],T[1]-1)
			print('moved tail:{},head={}'.format(T, H))
			reg(T)
		elif D=='U':
			H = (H[0]-1,H[1])
			if istouching(H,T):
				continue
			T = (T[0]-1,H[1])
			print('moved tail:{},head={}'.format(T, H))
			reg(T)
		elif D=='D':
			H = (H[0]+1,H[1])
			if istouching(H,T):
				continue
			T = (T[0]+1,H[1])
			print('moved tail:{},head={}'.format(T, H))
			reg(T)

ANS = len(V.keys())
# 7822
print("ANSWER ==>  {}\n".format(ANS))
