import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

ANS = 0
for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip('\n')
	for I in range(14,len(L)):
		if len(set(L[I-14:I])) == 14:
			ANS = I
			break


print("ANSWER ==>  {}\n".format(ANS))
