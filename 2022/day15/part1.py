import sys
import re

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
def dist(sensor):
	sx,sy,bx,by = sensor[0] + sensor[1]
	return abs(sx - bx) + abs(sy - by)

def get_imp_line(sensor, target_y):
	d = dist(sensor)
	sx,sy = sensor[0]
	dx = d - abs(target_y - sy)
	if dx <= 0:
		return None
	return [[sx - dx, sx + dx]]

def compress(target_y):
	y_lines = sorted(IMP[target_y], key=lambda l:l[0])
	new_lines = []
	tmp = None
	for i,l1 in enumerate(y_lines):
		if tmp is not None and tmp[1] >= l1[0]:
			continue
		tmp = l1
		new_lines.append(tmp)
		for l2 in y_lines[i+1:]:
			if tmp[1] < l2[0]:
				break
			tmp[1] = max(tmp[1], l2[1])
	IMP[target_y] = new_lines

def count(target_y):
	return sum([line[1] - line[0] + 1 for line in IMP[target_y]])

IMP={}
def add_line(target_y, new_line:tuple):
	if new_line is None:
		return
	if target_y not in IMP:
		IMP[target_y] = new_line
		return
	IMP[target_y] += new_line


TARGET_Y=10 if sys.argv[1] == 'tin' else 2000000
SENSORS = []
for l in LINES:
	sx,sy,bx,by = list(map(int, re.search(r"x=(\d+), y=(\d+):.*x=(-?\d+), y=(-?\d+)", l).groups()))
	SENSORS += [[[sx,sy],[bx,by]]]

for s in SENSORS:
	add_line(TARGET_Y, get_imp_line(s,TARGET_Y))

compress(TARGET_Y)
ANS = count(TARGET_Y)

if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
