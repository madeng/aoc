import sys

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
ANS = 0

# return, ((height,width), array of coordinates making up the shape)
add_line = lambda x,y:{(x,y),(x,y+1),(x,y+2),(x,y+3)}
add_plus = lambda x,y:{(x,y+1),(x+1,y),(x+1,y+1),(x+1,y+2),(x+2,y+1)}
add_rev_l = lambda x,y:{(x,y),(x,y+1),(x,y+2),(x+1,y+2),(x+2,y+2)}
add_letter_l = lambda x,y:{(x,y),(x+1,y),(x+2,y),(x+3,y)}
add_square = lambda x,y:{(x,y),(x,y+1),(x+1,y),(x+1,y+1)}

SHAPES = [
		((1,4), add_line),
		((3,3), add_plus),
		((3,3), add_rev_l),
		((4,1), add_letter_l),
		((2,2), add_square)
		]
NB_SHAPES = len(SHAPES)
MOVES = LINES[0]
NB_MOVES = len(MOVES)

LIMIT = 2022

dim = (0,0)
origin = [0,0]
nb_rocks = 0
nb_moves = 0
highest = 0
grid = set()
while nb_rocks < LIMIT:
	origin[0] = highest + 3
	origin[1] = 2

	dim,new_shape = SHAPES[nb_rocks % NB_SHAPES]
#	print("nb_rocks={}, origin={}, shape={}".format(nb_rocks,origin,nb_rocks%NB_SHAPES))
	while True:
		# Horizontal movement based on input
		new_origin = [o for o in origin]
		new_origin[1] += 1 if MOVES[nb_moves % NB_MOVES] == '>' else -1
#		print("pushing rock {}".format("left" if MOVES[nb_moves%NB_MOVES] == '<' else "right"))
		nb_moves += 1
		if 0 <= new_origin[1] and new_origin[1]+ dim[1] - 1 < 7:
			coords = new_shape(*new_origin)
			if grid.isdisjoint(coords):
#				print("moving origin from {} to {}".format(origin, new_origin))
				origin = new_origin

		# Move down if possible otherwise save the position and break
		if origin[0] == 0:
			coords = new_shape(*origin)
			grid |= coords
#			print("stopping at origin={}\n".format(origin))
			break

		origin[0] -= 1
		coords = new_shape(*origin)
		if not grid.isdisjoint(coords):
			origin[0] += 1
			coords = new_shape(*origin)
			grid |= coords
#			print("block found-stopping at origin={}\n".format(origin))
			break
	highest = max(highest, origin[0] + dim[0])
	nb_rocks += 1

ANS = highest
#
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
print('Done')
