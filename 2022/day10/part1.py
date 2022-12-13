import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))

REG=1
C=1
ANS = 0
for L in LINES:
	OP=L[:4]
	if OP == 'noop':
		C += 1
	elif OP == 'addx':
		TMP,VAL = L.split(" ")
		VAL = int(VAL)
		C += 1
		if (C + 20) % 40 == 0:
			ANS += REG * C
#			print('prev-adding {} to ans (reg={}, ans = {}, C={})'.format(REG*C, REG, ANS, C))
		C += 1
		REG += VAL

#		print ('addx by {}'.format(VAL))
	else:
		print('unknown op')
		break
	if (C + 20) % 40 == 0:
		ANS += REG * C
	#	print('adding {} to ans (reg={}, ans={}, C={})'.format(REG*(C), REG, ANS,C))


# 15140
print("ANSWER ==>  {}\n".format(ANS))
