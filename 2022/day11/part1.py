import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))

for L in LINES:
	pass


ANS = 0
#
print("ANSWER ==>  {}\n".format(ANS))
