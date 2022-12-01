import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

L=[]
T=[]
M=0
S=0
for DLINE in open(FILE):
	LINE = DLINE.strip()
	if LINE == '':
		if S > M:
			M = S
		T.append(S)
		S = 0
	else:
		S += int(LINE)
if S > 0:
	T.append(S)
	if S > M:
		M = S

#print(str(T))
print("1- top = {}".format(M))

T.sort(reverse=True)
TOP3 = T[0] + T[1] + T[2]
print("2- top3 = {}".format(TOP3))

