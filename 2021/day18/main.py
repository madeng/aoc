import sys
import re
from dataclasses import dataclass

infile = sys.argv[1] if len(sys.argv)>1 else 'input'

class SnailP:
	parent = None
	left = None
	right = None

	def __init__(self, parent, left, right):
		self.parent = parent
		self.right = right
		self.left = left
		if self.right is not None:
			self.right.parent = self
		if self.left is not None:
			self.left.parent = self
		
	def add(self, new):
		assert new is not None
		self.left = SnailP(self, self.left, self.right)
		self.right = new
		new.parent = self

	def replace(self, new):
		assert self.parent is not None
		assert new is not None
		
		new.parent = self.parent
		if self is self.parent.left:
			self.parent.left = new
		elif self is self.parent.right:
			self.parent.right = new
		else:
			assert False
		return new
		
	def check_explode(self, lvl=0):
		if self.left.is_leaf() and self.right.is_leaf() and lvl >= 4:
			return self
		for child in [self.left, self.right]:
			if not child.is_leaf():
				s = child.check_explode(lvl + 1)
				if s is not None:
					return s
		return None
		
	def check_split(self):
		for child in [self.left, self.right]:
			s = child.check_split()
			if s is not None:
				return s
		return None
		
	def magnitude(self):
		return (self.left.magnitude() *3) + (self.right.magnitude()*2)

	def is_leaf(self):
		return False

	def __str__(self):
		return "[{},{}]".format(self.left, self.right)

class SnailV:
	parent = None
	val = -1

	def __init__(self, parent, value):
		self.parent = parent
		self.val = value
		
	def replace(self, new):
		assert self.parent is not None
		assert new is not None
		
		new.parent = self.parent
		if self is self.parent.left:
			self.parent.left = new
		elif self is self.parent.right:
			self.parent.right = new
		else:
			assert False
		return new

	def check_split(self):
		if self.val > 9:
			return self
		return None

	def magnitude(self):
		return self.val

	def is_leaf(self):
		return True

	def __str__(self):
		return "{}".format(self.val)


def find_action(s) -> tuple:
	assert s is not None and s.is_leaf() == False
	assert s.left is not None and s.right is not None

	tmp = s.check_explode()
	if tmp is not None:
		return ("explode", tmp)

	tmp = s.check_split()
	if tmp is not None:
		return ("split", tmp)
		
	return (None, None)


def parse_line(s) -> SnailP:
	def build_snail(ancestor=None) -> SnailP:
		nonlocal offset, s
		assert len(s) >= 5
		assert s[offset] == "["

		ignored_chars = r"[,\]]"
		state = 0
		offset += 1
		cur_snail = SnailP(ancestor, None, None)
		while offset < len(s):
			c = s[offset]
			if re.match(ignored_chars, c):
				offset += 1
				continue

			if re.match(r"[0-9]", c):
				val = SnailV(cur_snail, int(c))
				offset += 1
			elif c == "[":
				val = build_snail(cur_snail)
			else:
				print("Unexpected char at {}: {}".format(offset, c))
				return None

			if state == 0:
				cur_snail.left = val
				state += 1
			elif state == 1:
				cur_snail.right = val
				return cur_snail
			else:
				print("invalid state!")
				return None
	offset = 0
	return build_snail()


def find_leaf(s, get_s):
	tmp_s = s
	last = tmp_s
	found = None
	while tmp_s.parent is not None:
		tmp_s = tmp_s.parent
		if get_s(tmp_s, "up") is not last:
			found = get_s(tmp_s,  "up")
			break
		last = tmp_s
		
	if found is not None:
		while not found.is_leaf():
			found = get_s(found, "down") 
		return found
	return None

def find_lleaf(s):
	return find_leaf(s, lambda t,d: t.left if d == "up" else t.right)

def find_rleaf(s):
	return find_leaf(s, lambda t,d: t.right if d == "up" else t.left)

def get_root(s): 
	assert s is not None
	while s.parent is not None:
		s = s.parent
	return s

def verify(s):
	assert s is not None
	if s.left.parent is not s:
		print("left is broken")
		print("s.left.parent",s.left.parent)
		print("s.left",s.left)
		print("s",s)
		assert False 
	if s.right.parent is not s:
		print("right is broken")
		print(s.right)
		print(s)
		assert False
	for child in [s.left,s.right]:
		if not child.is_leaf():
			verify(child)


def explode_snail(s):
	assert s is not None
	assert s.parent is not None
	assert not s.is_leaf()
	assert s.left.is_leaf() and s.right.is_leaf()
	
	l = find_lleaf(s)
	r = find_rleaf(s)
	if l is not None:
		l.val += s.left.val
	if r is not None:
		r.val += s.right.val
	new = s.replace(SnailV(s.parent, 0))
	return new

def split_snail(s):
	assert s is not None
	assert s.is_leaf()
	
	new = SnailP(s.parent, None, None)
	left = SnailV(new, s.val // 2)
	right = SnailV(new, s.val - left.val)
	new.left = left
	new.right = right
	return s.replace(new)

def reduce(s):
	action, snail = find_action(s)
	while action is not None:
		assert snail is not None
		if action not in ACTIONS:
			print("unknown action:", action)
			break
#		print("action =", action,", snail =", snail)
		ACTIONS[action](snail)
#		print("root", s)
		action, snail = find_action(s)
#		verify(s)

ACTIONS = {
	"explode": explode_snail,
	"split": split_snail,
}

line_list = []
ROOT = None
for line in open(infile):
#	print()
	line = line.strip()
	NEW = parse_line(line)
	line_list.append(line)
	verify(NEW)
	if ROOT is None:
		ROOT = NEW
	else:
		ROOT.add(NEW)
#	print("root",ROOT)
	verify(ROOT)
	reduce(ROOT)
#	print("after reduce,root", ROOT)

print("part1:", ROOT.magnitude())

max = 0
for i in range(len(line_list)):
	for j in range(len(line_list)):
		if i == j:
			continue
		S1 = parse_line(line_list[i])
		S2 = parse_line(line_list[j])
		S1.add(S2)
		reduce(S1)
		magnitude = S1.magnitude()
		if magnitude > max:
			max = magnitude

print("part2: ", max)