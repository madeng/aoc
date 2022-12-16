import sys
import re

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
ANS=0

MAX_X,MAX_Y = (20,20) if sys.argv[1] == 'tin' else (4000000,4000000)

def dist(sensor):
	sx,sy,bx,by = sensor[0] + sensor[1]
	return abs(sx - bx) + abs(sy - by)

def get_imp_line(sensor, target_y):
	d = dist(sensor)
	sx,sy = sensor[0]
	dx = d - abs(target_y - sy)
	if dx <= 0:
		return None
	return [sx - dx, sx + dx]

def compress():
	global IMP
	y_lines = sorted(IMP, key=lambda l:l[0])
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
	IMP = new_lines

def count():
	return sum([min(line[1],MAX_X) - max(line[0],0) + 1 for line in IMP])

IMP=None
def add_line(new_line:tuple):
	global IMP
	if new_line is None:
		return
	if IMP is None:
		IMP = [new_line]
	else:
		IMP.append(new_line)


SENSORS = []
for l in LINES:
	sx,sy,bx,by = list(map(int, re.search(r"x=(\d+), y=(\d+):.*x=(-?\d+), y=(-?\d+)", l).groups()))
	SENSORS += [[[sx,sy],[bx,by]]]

for y in range(0,MAX_Y+1):
	IMP=[]
	if y % 10000 == 0:
		print("check {}".format(y))
	for s in SENSORS:
		add_line(get_imp_line(s, y))

	compress()
	c = count()
	if c != MAX_X + 1:
		print("found count={} at line {}, imp={}".format(c,y,IMP))
		break

x = IMP[0][1] + 1
ANS = x * 4_000_000 + y
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
