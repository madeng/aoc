import sys
from functools import reduce

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
ANS = 0


class Monkey:
	def __init__(self, items=[], operation='', dividor=1, true_dest=None, false_dest=None):
		self.items = items
		self.dividor = dividor
		self.if_true = true_dest
		self.if_false = false_dest
		self.operation = operation
		self.inspected = 0

	def calc_new_item(self, index):
		val = self.operation[1]
		val = int(val) if val != 'old' else self.items[index]
		op = self.operation[0]
		if op == '+':
			self.items[index] += val
		elif op == '*':
			self.items[index] *= val
		self.items[index] = int(self.items[index])
		self.items[index] %= BIG_MOD
		self.inspected += 1
		return self.items[index]

	def test_item(self, index):
		return self.items[index] % self.dividor == 0

	def __repr__(self):
		return "items={},div={},if true={}, if_false={}, operation={}".format(
				str(self.items),
				self.dividor,
				self.if_true,
				self.if_false,
				self.operation
				)

ML = []
BIG_MOD = 1
for L in LINES:
	if L == '':
		pass
	elif L.startswith('Monkey'):
		M = Monkey()
		ML.append(M)
	elif 'Starting items:' in L:
		M.items = list(map(int, L.split(':')[-1].replace(' ','').split(",")))
	elif 'Operation:'  in L:
		M.operation = L.split(' ')[-2:]
	elif 'Test:' in L:
		M.dividor = int(L.split(' ')[-1])
		BIG_MOD *= M.dividor
	elif 'If true:' in L:
		M.if_true = int(L.split(' ')[-1])
	elif 'If false:' in L:
		M.if_false = int(L.split(' ')[-1])
#print(ML)


def solve():
	global ML
	for m in ML:
		while len(m.items) > 0:
			m.calc_new_item(0)
			if m.test_item(0):
				ML[m.if_true].items.append(m.items[0])
			else:
				ML[m.if_false].items.append(m.items[0])
			m.items.pop(0)


for _ in range(10000):
	solve()


INSPECT = [m.inspected for m in ML]
print(INSPECT)

ANS = reduce(lambda x,y: x*y, sorted(INSPECT)[-2:])
#
print("ANSWER ==>  {}\n".format(ANS))
