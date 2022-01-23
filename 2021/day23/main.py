import sys
import re
from heapq import *

DEBUG = False

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day23/input'
print("Reading from input file: {}".format(FILE))

class Pod:
    cost_per_type = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    type_to_room = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    def __init__(self, t: str):
        self.type = t
        self.move_cost = Pod.cost_per_type[t.capitalize()]
        self.assigned_room_id = Pod.type_to_room[t.capitalize()]

    def __repr__(self):
        return self.type


class Room:
    @classmethod
    def get_location(cls, id):
        return id * 2 + 2

    @classmethod
    def get_assigned_room(cls, room_list: list, pod: Pod):  # -> (int, Room):
        assigned_room = None
        for room in room_list:
            if room.id == pod.assigned_room_id:
                assigned_room = room
                break
        assert assigned_room is not None
        return assigned_room

    @classmethod
    def find_room_by_id(cls, room_list: list, id):  # ->Room:
        for room in room_list:
            if room.id == id:
                return room
        return None

    def __init__(self, id, size):
        self.id = id
        self.location = Room.get_location(id)
        self.size = size
        self.nbr_of_wrong_pods = 0
        self.is_ready = True
        self.pod_list = []
        self.is_finished = False

    def __str__(self):
        return str(self.pod_list)

    def __repr__(self):
        return self.__str__()

    def copy(self):
        new = Room(self.id, self.size)
        new.nbr_of_wrong_pods = self.nbr_of_wrong_pods
        new.is_ready = self.is_ready
        new.pod_list = self.pod_list.copy()
        new.is_finished = self.is_finished
        return new

    def peek(self) -> Pod:
        return self.pod_list[-1]

    def push(self, pod: Pod):
        nb_moves = self.size - len(self.pod_list)
        self.pod_list.append(pod)
        if pod.assigned_room_id != self.id:
            self.is_ready = False
        if not self.is_ready:
            self.nbr_of_wrong_pods += 1
        elif self.size == len(self.pod_list):
            self.is_finished = True
        return nb_moves

    def pop(self):
        assert self.is_finished is False
        pod = self.pod_list.pop()
        nb_moves = self.size - len(self.pod_list)
        if not self.is_ready:
            self.nbr_of_wrong_pods -= 1
            if self.nbr_of_wrong_pods == 0:
                self.is_ready = True
        return nb_moves, pod

    def reverse(self):
        old_pod_list = self.pod_list.copy()
        old_pod_list.reverse()
        self.__init__(self.id, self.size)
        [self.push(pod) for pod in old_pod_list]


class CorridorString:
    valid_pos = [0, 1, 3, 5, 7, 9, 10]
    size = 11
    empty_space = '.'

    def __init__(self, pod_list=None):
        if pod_list is None:
            self.pod_list = CorridorString.empty_space * CorridorString.size
        else:
            self.pod_list = pod_list

    def copy(self):
        return CorridorString(self.pod_list)

    def add(self, pod: Pod, from_pos: int, to_pos: int) -> int:
        assert self.pod_list[to_pos] == CorridorString.empty_space
        self.pod_list = self.pod_list[:to_pos] + pod.type + self.pod_list[to_pos + 1:]
        return abs(from_pos - to_pos)

    def remove(self, pod: Pod) -> int:
        assert pod in self.pod_list
        pod_pos = self.pod_list.find(pod.type)
        self.pod_list = self.pod_list[:pod_pos] + CorridorString.empty_space + self.pod_list[pod_pos + 1:]
        return abs(Room.get_location(pod.assigned_room_id) - pod_pos)

    def is_passage_free(self, from_pos, to_pos):
        if from_pos > to_pos:
            from_pos, to_pos = to_pos, from_pos
        from_pos += 1
        string = self.pod_list[from_pos:to_pos]
        if re.match(r".+", string):
            return True
        return False

    def get_free_space_from(self, room: Room):
        first_pos = room.location
        possible_space = [(first_pos - 1, lambda x: x - 1), (first_pos + 1, lambda x: x + 1)]
        free_space = []
        while len(possible_space) != 0:
            pos, direction = possible_space.pop()
            if 0 > pos or pos >= CorridorString.size:
                continue
            if pos not in CorridorString.valid_pos:
                possible_space.append((direction(pos), direction))
            elif self.pod_list[pos] == CorridorString.empty_space:
                free_space.append(pos)
                possible_space.append((direction(pos), direction))
        return free_space

    def get_pod(self, pos):
        c = self.pod_list[pos]
        if c == CorridorString.empty_space:
            return None
        return Pod(c)

    def reset_pos(self, pos):
        self.pod_list = self.pod_list[:pos] + CorridorString.empty_space + self.pod_list[pos + 1:]

    def __str__(self):
        return self.pod_list


class CorridorList:
    valid_pos = [0, 1, 3, 5, 7, 9, 10]
    size = 11

    def __init__(self, pod_list=None):
        if pod_list is None:
            self.pod_list = [None] * CorridorList.size
        else:
            self.pod_list = pod_list

    def __str__(self):
        tmp = ""
        for pod in self.pod_list:
            if pod is None:
                tmp += '.'
            else:
                tmp += pod.type
        return tmp

    def copy(self):
        return CorridorList(self.pod_list.copy())

    def add(self, pod: Pod, from_pos: int, to_pos: int) -> int:
        assert self.pod_list[to_pos] is None
        self.pod_list[to_pos] = pod
        return abs(from_pos - to_pos)

    def remove(self, pod: Pod) -> int:
        assert pod in self.pod_list
        pod_pos = self.pod_list.index(pod)
        del self.pod_list[pod_pos]
        return abs(Room.get_location(pod.assigned_room_id) - pod_pos)

    def is_passage_free(self, from_pos, to_pos):
        if from_pos > to_pos:
            from_pos, to_pos = to_pos, from_pos
        from_pos += 1
        for pod in self.pod_list[from_pos:to_pos]:
            if pod is not None:
                return False
        return True

    def get_free_space_from(self, room: Room):
        first_pos = room.location
        possible_space = [(first_pos - 1, lambda x: x - 1), (first_pos + 1, lambda x: x + 1)]
        free_space = []
        while len(possible_space) != 0:
            pos, direction = possible_space.pop()
            if 0 > pos or pos >= CorridorList.size:
                continue
            if pos not in CorridorList.valid_pos:
                possible_space.append((direction(pos), direction))
            elif self.pod_list[pos] is None:
                free_space.append(pos)
                possible_space.append((direction(pos), direction))
        return free_space

    def get_pod(self, pos):
        return self.pod_list[pos]

    def reset_pos(self, pos):
        self.pod_list[pos] = None


class Config:
    def __init__(self, is_finished: bool, room_list: list, corridor, cost: int):
        self.is_finished = is_finished
        self.cost = cost
        self.room_list = room_list
        self.corridor = corridor

    def __lt__(self, other):
        return self.cost < other.cost


def get_unfinished_room(room_list: list):
    unfinished = []
    finished = []
    for room in room_list:
        if not room.is_finished:
            unfinished.append(room)
        else:
            finished.append(room)
    return finished, unfinished


def get_moves_room_to_corridor(finished_room_list: list, unfinished_room_list, original_corridor) -> list:
    move_list = []
    for original_room in unfinished_room_list:
        if original_room.is_ready:
            continue
        free_space_list = original_corridor.get_free_space_from(original_room)
        if len(free_space_list) == 0:
            continue
        new_room = original_room.copy()
        r_cost, pod = new_room.pop()
        new_room_list = unfinished_room_list.copy()
        new_room_list.remove(original_room)
        new_room_list.append(new_room)
        new_room_list.extend(finished_room_list)
        for free_space in free_space_list:
            new_corridor = original_corridor.copy()
            c_cost = new_corridor.add(pod, new_room.location, free_space)
            move_list.append(Config(False, new_room_list, new_corridor, pod.move_cost * (r_cost + c_cost)))
    return move_list


def get_moves_room_to_room(finished_room_list: list, unfinished_room_list, corridor) -> list:
    move_list = []
    for i, original_room in enumerate(unfinished_room_list):
        if original_room.is_ready:
            continue
        pod = original_room.peek()
        room_dest = Room.get_assigned_room(unfinished_room_list, pod)
        if not room_dest.is_ready:
            continue
        if corridor.is_passage_free(original_room.location, Room.get_location(pod.assigned_room_id)):
            new_room_list = unfinished_room_list.copy()
            new_room_list.pop(i)
            new_room_list.remove(room_dest)
            new_room_source = original_room.copy()
            new_room_dest = room_dest.copy()
            new_room_list.append(new_room_source)
            new_room_list.append(new_room_dest)
            r_cost1, pod = new_room_source.pop()
            r_cost2 = new_room_dest.push(pod)
            c_cost = abs(new_room_source.location - new_room_dest.location)
            new_room_list.extend(finished_room_list)
            move_list.append(Config(False, new_room_list, corridor, pod.move_cost * (r_cost1 + c_cost + r_cost2)))
            return move_list
    return move_list


def get_moves_corridor_to_room(finished_room_list: list, unfinished_room_list: list, corridor) -> list:
    move_list = []
    for pos in range(corridor.size):
        pod = corridor.get_pod(pos)
        if pod is None:
            continue
        room_dest = Room.get_assigned_room(unfinished_room_list, pod)
        if not room_dest.is_ready:
            continue
        if corridor.is_passage_free(pos, room_dest.location):
            new_room_list = unfinished_room_list.copy()
            new_room_list.remove(room_dest)
            new_room = room_dest.copy()
            new_room_list.append(new_room)
            new_corridor = corridor.copy()
            new_corridor.reset_pos(pos)
            r_cost = new_room.push(pod)
            c_cost = abs(pos - new_room.location)
            is_finished = False
            if len(unfinished_room_list) == 1 and new_room.is_finished:
                is_finished = True
            new_room_list.extend(finished_room_list)
            move_list.append(Config(is_finished, new_room_list, new_corridor, pod.move_cost * (c_cost + r_cost)))
            return move_list
    return move_list


def find_moves(room_list: list, corridor) -> list:
    finished_room_list, unfinished_room_list = get_unfinished_room(room_list)
    # Returns the best, unavoidable moves.
    # This avoids branching in many directions when it does not make sense to think about it
    c2r_moves = get_moves_corridor_to_room(finished_room_list, unfinished_room_list, corridor)
    if len(c2r_moves) != 0:
        return c2r_moves
    r2r_moves = get_moves_room_to_room(finished_room_list, unfinished_room_list, corridor)
    if len(r2r_moves) != 0:
        return r2r_moves
    return get_moves_room_to_corridor(finished_room_list, unfinished_room_list, corridor)


def print_config(room_list: list, corridor):
    assert len(room_list) != 0
    room_size = room_list[0].size
    nb_lines = room_size + 3
    for x in range(nb_lines):
        if x == 1:
            print("#{}#".format(corridor))
        elif x == 0 or x > 1:
            room_id = 0
            for y in range(corridor.size + 2):
                if x == 0 or \
                        x == nb_lines - 1 and 2 < y < 11 or \
                        0 < y < 11 and y % 2 == 0 or \
                        x == 2 and (y < 3 or y > 9):
                    print("#", end="")
                elif 2 < y < 10:
                    room = Room.find_room_by_id(room_list, room_id)
                    pod_list = room.pod_list if room is not None else None
                    index = 1 + room_size - x
                    if pod_list is None or index >= len(pod_list):
                        print('.', end="")
                    else:
                        print(pod_list[index], end="")
                    room_id += 1
                else:
                    print(" ", end="")
            print()  # new line


def sanity_check(config: Config):
    # Check the number of pods
    nbr_of_pods = 0
    for pod in config.corridor.pod_list:
        if pod is not None:
            nbr_of_pods += 1

    for room in config.room_list:
        nbr_of_pods += len(room.pod_list)
    assert nbr_of_pods == 8


# The minimum move cost would be moving a 'A' into the A column when it is in the corridor right out of the room 'A'
MIN_MOVE_COST = 2


def solve(room_list: list) -> int:
    config_heap = []
    heappush(config_heap, Config(False, room_list, Corridor(), 0))
    counter = 0
    min_cost = 1000000000
    while len(config_heap) != 0:
        config = heappop(config_heap)
        if DEBUG:
            counter += 1
            print("\npopped (count={}, cost={}):".format(counter, config.cost))
            print_config(config.room_list, config.corridor)
        if config.cost >= min_cost - MIN_MOVE_COST:
            # No point in looking into this config. We would have at least the same min_cost if not more.
            continue
        new_config_list = find_moves(config.room_list, config.corridor)
        for new_config in new_config_list:
            if DEBUG:
                counter += 1
                print("\nnew config (count={}, cost={}):".format(counter, config.cost + new_config.cost))
                print_config(new_config.room_list, new_config.corridor)
                sanity_check(new_config)
            new_config.cost += config.cost
            if new_config.cost >= min_cost:
                continue
            if new_config.is_finished:
                min_cost = new_config.cost
                continue
            heappush(config_heap, new_config)
    return min_cost

############ CLASS CHOICE
Corridor = CorridorList
############

ROOM_SIZE_PART1 = 2
# POD_PER_TYPE = []
ROOM_LIST1 = [
    Room(0, ROOM_SIZE_PART1),
    Room(1, ROOM_SIZE_PART1),
    Room(2, ROOM_SIZE_PART1),
    Room(3, ROOM_SIZE_PART1)
]
for X, LINE in enumerate(open(FILE)):
    LINE = LINE.strip("\n")
    if 2 > X > 3:
        # Only the rooms are not empty at the beginning
        continue
    for Y, C in enumerate(LINE):
        if (Y == 3 or Y == 5 or Y == 7 or Y == 9) and re.match(r'[A-Da-d]', C) is not None:
            POD = Pod(C)
            ROOM = ROOM_LIST1[(Y - 3) // 2]
            ROOM.push(POD)

[R.reverse() for R in ROOM_LIST1]
print(str(ROOM_LIST1))

print("part1: x = {}".format(solve(ROOM_LIST1)))

ROOM_SIZE_PART2 = 4
ROOM_LIST2 = [
    Room(0, ROOM_SIZE_PART2),
    Room(1, ROOM_SIZE_PART2),
    Room(2, ROOM_SIZE_PART2),
    Room(3, ROOM_SIZE_PART2)
]
for room2 in ROOM_LIST2:
    room1 = Room.find_room_by_id(ROOM_LIST1, room2.id)
    room2.push(room1.pod_list[0])
    if room2.id == 0:
        room2.push(Pod('D'))
        room2.push(Pod('D'))
    elif room2.id == 1:
        room2.push(Pod('B'))
        room2.push(Pod('C'))
    elif room2.id == 2:
        room2.push(Pod('A'))
        room2.push(Pod('B'))
    elif room2.id == 3:
        room2.push(Pod('C'))
        room2.push(Pod('A'))
    else:
        assert False
    room2.push(room1.pod_list[1])

print("part2: x = {}".format(solve(ROOM_LIST2)))
