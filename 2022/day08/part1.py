import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

ANS = 0
for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip('\n')


print("ANSWER ==>  {}\n".format(ANS))
