import sys
import math

infile = sys.argv[1] if len(sys.argv)>1 else 'in'

def reverse_sum(n) ->float:
	return (-1 + pow(1 + 8*n, 1/2)) / 2

def int_sum(n):
	return int(n*(n+1)/2)

def step(pos:tuple, speed:tuple) -> (tuple, tuple):
	x,y = pos
	xspeed, yspeed = speed
	new_x_speed = xspeed - 1 if xspeed > 0 else 0
	return ((x + xspeed, y + yspeed), (new_x_speed, yspeed - 1))

def print_trace(trace):
	max_y = 0
	for x,y in trace.keys():
		max_y = max(max_y, y)
		
	for y in range(max_y, TY1-1,-1):
		for x in range(TX2+1):
			other = "T" if TX1 <= x <= TX2 and TY1<= y <= TY2 else "."
			print(trace[(x,y)] if (x,y) in trace.keys() else other, end="")
		print()

def verify_speed(initial_speed:tuple) -> bool:
	pos = S
	show_trace = False
	trace={}
	trace[pos] = "S"
	speed = initial_speed
	while pos[0] <= TX2 and pos[1] >= TY1:
		if pos[0] >= TX1 and pos[1] <= TY2:
#			if pos[0] == TX1 and pos[1] == TY2:
#				print("value found for ({},{})".format(TX1, TY2))
			if show_trace:
				print(initial_speed)
				print_trace(trace)
			return True
		pos, speed = step(pos, speed)
		trace[pos] = "#"

	return False

S=(0,0)

for line in open(infile):
	TX,TY = line.strip().split(':')[1].split(',')
	print(line)
	TX1,TX2 = [int(n) for n in TX.split("=")[1].split("..")]
	TY1,TY2 = [int(n) for n in TY.split("=")[1].split("..")]

	MIN_VX = math.ceil(reverse_sum(TX1))
	MAX_VX = TX2
	MIN_VY = TY1
	MAX_VY = -TY1 - 1 # To reach maximum altitude (part1)
	print("part1: {}".format(int_sum(MAX_VY)))

	# Part 2
	velocity_list = []
	m={}
	for vy in range(MAX_VY, MIN_VY -1, -1):
		for vx in range(MIN_VX, MAX_VX + 1):
			if verify_speed((vx, vy)):
				velocity_list.append((vx,vy))
				m[(vx,vy)] = True
			else:
				m[(vx,vy)] = False

	print("part2:", len(velocity_list))

	for y in range(MAX_VY, MIN_VY - 1, -1):
		print()
		print("{0: >4}".format(y), end="")
		for x in range(MAX_VX + 1):
			c = " "
			if x >= MIN_VX and m[(x,y)]:
				c = "X"
			elif x == 0:
				c = "|"
			elif y == 0:
				c = "_"
			elif y == -1:
				c = str(x%10) if x %5 ==0 else " "
			print(c, end="")