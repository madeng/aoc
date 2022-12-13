import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
LX = len(LINES)
LY = len(LINES[0])
ANS = 0


S = list(filter(lambda x: x[1] != -1, [(i,l.find('S')) for i,l in enumerate(LINES)]))[0]

def char(n:tuple):
	c = LINES[n[0]][n[1]]
	if c == 'S':
		return 'a'
	return c

def ascii(n:tuple):
	return ord(char(n))

def solve(start):
	global LX,LY,S,LINES
	found = False
#	print("solve for {}".format(start))
	cost = {}
	cost[start] = 0
	queue = [start]
	end = None
	while len(queue) > 0:
		n = queue.pop(0)
		#print("\npopped {}=={}".format(n,char(n)))
		char_origin = char(n)
		ascii_origin = ord(char_origin)
		for coord in [\
				(n[0]+1,n[1]), \
				(n[0]-1,n[1]), \
				(n[0],n[1]+1), \
				(n[0],n[1]-1)]:
			if not(-1 < coord[0] < LX and -1 < coord[1] < LY) \
					or coord in cost:
				#print("{}, out of bounds or in cost".format(coord))
				continue

			#print("checking {}=={}".format(coord,char(coord)))
			if (char_origin == 'y' or char_origin == 'z') and char(coord) == 'E' \
					or ascii(coord) - ascii_origin <= 1:
				#print("adding it")
				cost[coord] = cost[n] + 1
				queue.append(coord)
				if char(coord) == 'E':
					end = coord
					found = True
					break


		if found: break

#	tmp=''
#	for x in range(LX):
#		tmp += str(x +2)
#		tmp += ' ' if x > 9 else '  '
#		for y in range(LY):
#			tmp += '-' if (x,y) not in cost else char((x,y))
#		tmp+='\n'
	#print(tmp)
	return cost[end] if end is not None else 10000

results = [10000 if char((x,y)) != 'a' else solve((x,y)) for y in range(LY) for x in range(LX)]
print(results)
ANS = min(results)
#
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
