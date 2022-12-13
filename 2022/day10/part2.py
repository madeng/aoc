import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))

REG=1
C=0
ANS = 0
TMP = ''

def printpixel(p):
	global TMP
	c = '.' if p not in [REG-1,REG,REG+1] else '#'
#	print('drawing pixel {}, sprite at {}, char={}'.format(p, REG,c))
	print(c, end='')
#	TMP += c

def tick():
	global REG,C,ANS
	printpixel(C % 40)
	C += 1
	if C % 40 == 0:
		print('\n',end='')

for L in LINES:
	OP=L[:4]
#	print('cycle {}: executing {}'.format(C, L))
	if OP == 'noop':
		tick()
	elif OP == 'addx':
		TMP,VAL = L.split(" ")
		VAL = int(VAL)
		tick()
		tick()
		REG += VAL
#		print ('addx by {}'.format(VAL))
	else:
		print('unknown op')
		break
	#	print('adding {} to ans (reg={}, ans={}, C={})'.format(REG*(C), REG, ANS,C))

# 13140
print("ANSWER ==>  {}\n".format(ANS))
