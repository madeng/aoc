from functools import reduce
import sys
import ast

#strip = lambda x : x.strip('\n')
#LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
LINES = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read()
ANS = 0

DEBUG = False
def out(*args):
	if DEBUG:
		print(args)

def check(p1,p2):
	out('comparing', p1,'(',str(type(p1)),')','vs',p2,'(',str(type(p2)),')')
	if isinstance(p1, list) or isinstance(p2, list):
		if not isinstance(p1, list):
			p1 = [p1]
		elif not isinstance(p2,list):
			p2 = [p2]

		for item1,item2 in zip(p1,p2):
			retval = check(item1,item2)
			if retval is not None:
				out('GOOD' if retval == True else 'False', 'sub-result')
				return retval
		# No decision was made, so compare the length of the list
		if len(p1) > len(p2):
			out('BAD length of p1 is bigger than p2')
			return False
		elif len(p2) > len(p1):
			out('GOOD length of p2 is bigger than p1')
			return True
		else:
			return None
	else:
		retval = True if p1 < p2 else False if p2 < p1 else None
		if retval is not None:
			out('GOOD' if retval == True else 'BAD' if retval==False else '', p1,'vs',p2)
		return retval

CORRECT=[]
for g_index,group in enumerate(LINES.split('\n\n')):
	p1,p2 = map(ast.literal_eval, group.split('\n')[:2])
	out()
	out(g_index, p1)
	out(g_index, p2)
	if check(p1,p2):
		CORRECT.append(g_index + 1)
		out(g_index, 'is correct')


ANS = reduce(lambda x,y:x+y, CORRECT)
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
