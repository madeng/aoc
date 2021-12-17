
# Example
#test_input_paths = ['testinput', 'testinput2', 'testinput3']
from datetime import datetime

test_input_paths = ['testinput']
test_expected_results = [315]

input_path = 'input'
expected_result = None

class Node:
    coord = None
    distance = None
    parent = None
    def __init__(self, coord: tuple, parent, distance):
        self.coord = coord
        self.parent = parent
        self.distance = distance

    def __eq__(self, other):
        if type(other) != Node:
            return False
        return True if self.coord == other.coord and self.distance == other.distance else False

    def __hash__(self):
        global W, H
        return self.distance * W * H + self.coord[0] * W + self.coord[1]

    def show_path(self) -> str:
        path = "{}".format(self.coord)
        parent = self.parent
        while parent is not None:
            path += ",{}".format(parent.coord)
            parent = parent.parent
        return path


def neighbors(coord: tuple):
    global W, H
    _neighbors = [(coord[0],coord[1] - 1),(coord[0] - 1,coord[1]),
                  (coord[0] + 1, coord[1]), (coord[0], coord[1] + 1)]
    return [n for n in _neighbors if 0 <= n[0] < H and 0 <= n[1] < W]


H = None  # Height of input (number of lines), coord[0]
W = None  # width of lines, coord[1]
def part(file_path: str) -> int:
    global H, W
    m = {}
    W = None
    H = None
    for line_no,line in enumerate(open(file_path).read().split("\n")):
        if W is None:
            W = len(line)
        if line == '':
            break
        H = line_no + 1
        for i, c in enumerate(line):
            m[(line_no, i)] = int(c)

    for y in range(0, H):
        for x in range(0, W):
            for j in range(0, 5):
                for i in range(0, 5):
                    if i == 0 and j == 0:
                        continue
                    v = i + j + int(m[y,x])
                    m[(y + j * H, x + i * W)] = v if v < 10 else v - 9

    H *= 5
    W *= 5
    # for y in range(0, H):
    #     for x in range(0, W):
    #         print(m[y,x], end='')
    #     print()

    min_d = m[(0, 0)]
    s = Node((0,0), None, min_d)

    n_per_d = {min_d: set([s])}
    consumed_coords = {}
    end = (H - 1, W - 1)
    has_reached_end = False
    f = None # Final path
    count = 0
    while not has_reached_end:
        sp = n_per_d[min_d].pop()  # shortest path
        for n in neighbors(sp.coord):
            if n in consumed_coords:
                continue
            dist = min_d + m[n]
            new_node = Node(n, sp, dist)
            if n == end:
                f = new_node
                has_reached_end = True
            if dist not in n_per_d:
                n_per_d[dist] = set()
            n_per_d[dist].add(new_node)
        consumed_coords[sp.coord] = None
        if len(n_per_d[min_d]) == 0:
            n_per_d.pop(min_d)
            min_d = min(n_per_d.keys())

        # count += 1
        # if count > 100000:
        #     count = 0
        #     print("sp.coord={}, nodes with min_d={}, len(consumed_coord)={}, shortest dist so far={}".format(
        #         sp.coord, len(n_per_d[min_d]), len(consumed_coords), min_d))

    return dist - m[s.coord]


def do_part_test( ) -> bool:
    is_success =True
    for index,  file_path in enumerate(test_input_paths):
        result = part(file_path)
        test_expected_result = test_expected_results[index]
        if result != test_expected_result:
            print("1-Failure in test {}. Result is {}, expected {}".format(test_input_paths, result, test_expected_result))
            is_success = False
        else:
            print("1-Test success! Got {}, expected {}".format(result, test_expected_result))
    return is_success

def do_part():
    result = part(input_path)
    if expected_result is not None:
        if expected_result != result:
            print("1-wrong final result: {}".format(result))
        else:
            print("1-Correct final result: {}".format(result))
        return
    print("1-final result: {}".format(result))


if do_part_test():
    start = datetime.now()
    do_part()
    end = datetime.now()
    print(end - start)
