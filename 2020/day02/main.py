import sys
import re

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

OK1 = 0
OK2 = 0
for LINE in open(FILE):
	R, C, PWD = LINE.strip().split(' ')
	C = C[0]
	R1,R2 = [int(n) for n in R.split('-')]

	if R1 <= len(re.findall(C, PWD)) <= R2:
		OK1 += 1

	SUB = PWD[R1 - 1] + PWD[R2 - 1]
	if len(re.findall(C, SUB)) == 1:
		OK2 +=1

print(OK1)
print(OK2)
