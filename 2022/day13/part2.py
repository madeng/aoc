from functools import reduce
from functools import cmp_to_key
import sys
import ast

#strip = lambda x : x.strip('\n')
#LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
LINES = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read()

def check(p1,p2):
	if isinstance(p1, list) or isinstance(p2, list):
		if not isinstance(p1, list):
			p1 = [p1]
		elif not isinstance(p2,list):
			p2 = [p2]

		for item1,item2 in zip(p1,p2):
			retval = check(item1,item2)
			if retval != 0:
				return retval
		return 1 if len(p1) > len(p2) else -1 if len(p2) > len(p1) else 0
	else:
		return -1 if p1 < p2 else 1 if p2 < p1 else 0

packets = []
for g_index,group in enumerate(LINES.split('\n\n')):
	p1,p2 = map(ast.literal_eval, group.split('\n')[:2])
	packets.append(p1)
	packets.append(p2)

div1 = "[[2]]"
div2 = "[[6]]"
packets += list(map(ast.literal_eval,[div1, div2]))
packets.sort(key=cmp_to_key(check))
res = [i+1 if str(p) == div1 or str(p) == div2 else 1 for i,p in enumerate(packets)]

print("ANSWER ==>  {}\n".format(reduce(lambda x,y:x*y,res)))
