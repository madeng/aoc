import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

FIRST_PART=True
ISTATE=[]
STEPS=[]
for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip('\n')
	if L == '':
		FIRST_PART = False
	elif FIRST_PART:
		ISTATE.append(L)
	else:
		STEPS.append(L)
ISTATE.pop() # Remove useless lines with numbers

NB_CONT = int((len(ISTATE[0])+1)/4)
S = []
[S.append([]) for i in range(NB_CONT)]
for L in ISTATE:
	for S_I in range(NB_CONT):
		CONT = L[S_I*4+1]
		if CONT == ' ':
			continue
		S[S_I].insert(0,CONT)

for L in STEPS:
	NB,SRC,DEST = [int(s) for s in L.split(' ') if s.isnumeric()]
	SRC-=1
	DEST-=1

	S[DEST].extend(S[SRC][-NB:])
	[S[SRC].pop() for n in range(NB)]

P2 = ''.join([stack[-1] for stack in S])

print("({}) Part 2 ==>  {}\n".format(FILE, P2))
