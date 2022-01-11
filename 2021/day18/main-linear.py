import sys
import re
from dataclasses import dataclass

infile = sys.argv[1] if len(sys.argv)>1 else 'testinput'

def rewind(s):
	assert s is not None
	while s.prev is not None:
		s = s.prev
	return s


def print_snail(s):
	while s is not None:
		print(s, end="")
		s = s.next
	print()
	return True
	

class Snail:
	prev = None
	next = None
	val = None
	lvl = 0
	type = None

	def __init__(self, value, level, type, prev=None, next=None):
		assert type == "left" or type == "right"
		
		self.val = value
		self.lvl = level
		self.type = type
		self.prev = prev if prev is not None else self.prev
		self.next = next if next is not None else self.next

	def __str__(self):
		str = "{}".format(self.val)
		if self.type == "left":
			br = max(1, self.lvl - self.prev.lvl) if self.prev is not None else self.lvl
			for _ in range(br):
				str = "[" + str
			if self.next is None:
				for _ in range(self.lvl):
					str = str + "]"
			else:
					str = str + ","
		else:
			br = max(1, self.lvl - self.next.lvl) if self.next is not None else self.lvl
			for _ in range(br):
				str = str + "]"
			str = str + "," if self.next is not None else str
		return str


def parse_line(s):
	level = 0
	snail_list = []
	for c in s:
		if c =="[":
			level +=1
			type = "left"
		elif c =="]":
			level -= 1
		elif c==",":
			type="right"
		elif re.match(r"[0-9]", c):
			snail_list.append(Snail(int(c),level,type))
			
	for prev,next in zip(snail_list, snail_list[1:]):
		prev.next = next
		next.prev = prev
	
	return snail_list


def find_action(s):
	orig = s
	while s is not None:
		if s.next is not None and s.lvl > 4 and s.next.lvl == s.lvl and s.type == "left" and s.next.type=="right":
			return ("explode", s)
		if s.val > 9: 
			return ( "split", s)
		s = s.next
	return (None, orig)


def explode_snail(s):
	left = s
	right = s.next
	assert left is not None and right is not None
	assert left.type == "left"
	assert right.type == "right" or (print_snail(s) and print("type is not right")   and False)
	assert left.lvl == right.lvl
	
	new = Snail(0, left.lvl - 1, "left")
	if left.prev is not None:
		new.type = "right" if left.prev.type == "left" else new.type
		left.prev.val += left.val
		left.prev.next = new
		new.prev = left.prev
		
	if right.next is not None:
		right.next.val += right.val
		right.next.prev = new
		new.next = right.next
		
	return rewind(new)
	

def split_snail(s):
	assert s is not None
	assert s.val > 9
	
	oldval = s.val
	s.lvl += 1
	s.val = oldval // 2
	new = Snail(oldval - s.val, s.lvl, "right", s, s.next)
	s.next = new
	s.type = "left"
	return rewind(s)
	
	
def add(s1, s2):
	assert s1 is not None and s2 is not None
	s = s1
	while s is not None:
		s.lvl += 1
		last = s
		s = s.next
	last.next = s2
	s= s2
	while s is not None:
		s.lvl += 1
		s  = s.next
	return s1

def reduce(s):
	assert s is not None
	action, s = find_action(s)
	assert s is not None
	while action is not None:
		assert action in ACTIONS
		print("doing action '{}'".format(action))
		s = ACTIONS[action](s)
		assert s is not None
		print_snail(s)

		action, s = find_action(s)
		assert s is not None

	return rewind(s)


ACTIONS = {
	"explode": explode_snail,
	"split": split_snail,
}

S_LIST = []
for line in open(infile):
	line = line.strip()
	print()
	print(line)
	S_LIST = parse_line(line)[0]
	print_snail(S_LIST)
	S_LIST.append(S_LIST)



print("addition")
G = S_LIST[0]
for S_LIST in S_LIST[1:]:
	G = add(G, S_LIST)
	print_snail(G)
	
G = reduce(G)
print("final G")
print_snail(G)