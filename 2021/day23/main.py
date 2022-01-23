# cython: language_level=3
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day23/input'
print("Reading from input file: {}".format(FILE))

TYPES_TO_INDEX = {'A':0, 'B':1, 'C':2, 'D':3, '.':-1}
# class Pod:
    # def __init__(self, pos, t):
    #     self.origin = pos
    #     self.pos = pos
    #     self.type = t
    #
    # def move(self, new_pos):
    #     self.type
    #
    # def is_in_room(self):
    #     if 2 > self.pos[0] > 3:
    #         return False
    #     return True
    #
    # def is_in_correct_room(self):
    #     if not self.is_in_room():
    #         return False
    #     if self.pos[1]:
    #         pass
    #
    # # The difference between two pod can be calculated if they are the same Pod at two different times in its existence.
    # # This would mean the difference between its position to be able to calculate the cost.
    # def __sub__(self, other:Pod):
    #     assert other.origin == self.origin
    #     return self.pos[0] + self.pos[1] - other.pos[0] - other.pos[1]
    #
    # def __repr__(self):
    #     return "[{},({},{}]".format(self.type, self.pos[0],self.pos[1])
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return self.x * 100 + self.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

class Movement:
    COST_PER_TYPE = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }
    
    def __init__(self, t, pos_before:tuple, pos_after:tuple):
        self.pos_before = pos_before
        self.pos_after = pos_after
        self.type = t
        diff = abs(pos_after[0] - pos_before[0]) + abs(pos_after[1] - pos_before[1])
        self.cost = Movement.COST_PER_TYPE[self.type] * diff


def print_config(config:dict):
    dim_y = 13
    dim_x = 5
    for x in range(dim_x):
        print(x, end='')
        for y in range(dim_y):
            if x == 0:
                print(y % 10, end='')
                continue
            if (x,y) in config.keys():
                print(config[(x,y)], end='')
        print()

def is_solved(config:dict):
    # print_config(config)
    for i,room in enumerate(ROOM_Y_LIST):
        if TYPES_TO_INDEX[config[(2, room)]] != i or TYPES_TO_INDEX[config[(3, room)]] != i:
            return False
    return True

# Check if the corridor is free between two y positions (excluding those positions).
def is_corridor_free_between(y1, y2, config):
    if y1 > y2:
        y1, y2 = y2, y1
    for y in range(y1 + 1, y2):
        if config[(1,y)] != '.':
            return False
    return True

def get_possible_movements(config:dict, from_pod_pos:tuple):
    initial_x, initial_y = from_pod_pos
    pod_type = config[from_pod_pos]
    room_y_index = TYPES_TO_INDEX[pod_type]
    room_y = ROOM_Y_LIST[room_y_index]
    if initial_x > 1:  # From a room, the corridor is the only option
        # Check if the pod is already in the right position, 'cause it would be useless to move it if it was the case.
        if initial_y == room_y:  # Pod is in the right room
            if initial_x == 3:  # pod is at bottom of room, that is correct
                return []
            else:  # pod is at the top of the room
                # Check if the other pod at the bottom is of the correct type.
                if config[(3,initial_y)] == pod_type:
                    return []
        new_x = 1  # corridor
        # Check that it is possible to get out of room if the pod is at the bottom of the room
        if initial_x == 3 and config[(2,initial_y)] != '.':
            return []
        possibilities_incr = [(new_x, initial_y + 1)]
        possibilities_decr = [(new_x, initial_y - 1)]
        possible_movements = []
        while len(possibilities_incr) > 0:
            pos = possibilities_incr.pop()
            if config[pos] == '.':
                if pos[1] not in ROOM_Y_LIST:
                    possible_movements.append(pos)
                possibilities_incr.append((pos[0],pos[1] + 1))
        while len(possibilities_decr) > 0:
            pos = possibilities_decr.pop()
            if config[pos] == '.':
                if pos[1] not in ROOM_Y_LIST:
                    possible_movements.append(pos)
                possibilities_decr.append((pos[0], pos[1] - 1))
        return possible_movements
    else:  # Already in corridor
        coord_bottom_room = (3, room_y)
        # Check that the bottom of the room is free or occupied by the correct type of pod and that the second spot
        # is free.
        if config[coord_bottom_room] == pod_type:
            coord_top_room = (2, room_y)
            if config[coord_top_room] == '.':
                if is_corridor_free_between(room_y, initial_y, config):
                    return [coord_top_room]
        elif config[coord_bottom_room] == '.':
            if is_corridor_free_between(room_y, initial_y, config):
                return [coord_bottom_room]
    return []


def solve(config:dict, movement_list:list):
    if is_solved(config):
        return sum([m.cost for m in movement_list])

    # print_config(config)
    min_cost = 1000000000
    for x in range(1,3 + 1):
        for y in range(1,11 + 1):
            if x > 1 and y not in ROOM_Y_LIST:
                continue
            c = config[(x, y)]
            if c == '.':
                continue
            for new_pod_pos in get_possible_movements(config, (x,y)):
                # print_config(config)
                # Add move to movement list
                new_movement_list = movement_list.copy()
                new_movement_list.append(Movement(c, (x,y), new_pod_pos))
                # Update configuration by moving the pod to its new place
                new_config = config.copy()
                new_config[(x,y)] = '.'
                new_config[new_pod_pos] = c
                cost = solve(new_config, new_movement_list)
                if cost < min_cost:
                    min_cost = cost
    return min_cost


FREE_SPOT = []
ROOM_Y_LIST = [3, 5, 7, 9]
INITIAL_CONFIG = {}
for X,LINE in enumerate(open(FILE)):
    LINE = LINE.strip("\n")
    for Y,C in enumerate(LINE):
        INITIAL_CONFIG[(X,Y)] = C

print("part1: x = {}".format(solve(INITIAL_CONFIG, [])))

# print("part2: x = {}".format())
