import sys
import math

infile = sys.argv[1] if len(sys.argv)>1 else '17.in'

def reverse_sum(n) ->float:
    return (-1 + pow(1 + 8*n, 1/2)) / 2

def int_sum(n):
    return int(n*(n+1)/2)

def step(pos:tuple, speed:tuple) -> (tuple, tuple):
    x,y = pos
    xspeed, yspeed = speed
    new_x_speed = xspeed - 1 if xspeed > 0 else 0
    return ((x + xspeed, y + yspeed), (new_x_speed, yspeed - 1))

def verify_speed(initial_speed:tuple) -> bool:
    pos = S
    speed = initial_speed
    while pos[0] <= TX2 and pos[1] >= TY1:
        if pos[0] >= TX1 and pos[1] <= TY2:
            return True
        pos, speed = step(pos, speed)
    return False

S=(0,0)

for line in open(infile):
    TX,TY = line.strip().split(':')[1].split(',')
    TX1,TX2 = [int(n) for n in TX.split("=")[1].split("..")]
    TY1,TY2 = [int(n) for n in TY.split("=")[1].split("..")]

    MIN_VX = math.ceil(reverse_sum(TX1))
    MAX_VX = TX2
    MIN_VY = TY1
    MAX_VY = -TY1 - 1 # To reach maximum altitude (part1)
    print("part1: {}".format(int_sum(MAX_VY)))

    # Part 2
    velocity_list = []
    for vx in range(MIN_VX, MAX_VX + 1):
        for vy in range(MIN_VY, MAX_VY + 1):
            if verify_speed((vx, vy)):
                velocity_list.append((vx,vy))

    print("part2:", len(velocity_list))


