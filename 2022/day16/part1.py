import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
ANS = 0


#
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
