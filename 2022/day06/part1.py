import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

ANS = 0
for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip('\n')
	for I in range(4,len(L)):
		if len(set(L[I-4:I])) == 4:
			ANS = I
			break


print("ANSWER ==>  {}\n".format(ANS))
