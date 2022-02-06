import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

L=[]
for LINE in open(FILE):
    L.append(int(LINE.strip()))

for I,N1 in enumerate(L):
	for J in range(I+1,len(L)):
		N2 = L[J]
		if N1 + N2 == 2020:
			print("1st part:", N1 * N2)
		for Z in range(J+1, len(L)):
			N3 = L[Z]
			if N1 + N2 + N3 == 2020:
				print("2nd part:", N1 * N2 * N3)

