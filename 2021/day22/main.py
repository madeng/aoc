import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day22/in'

class Cube:
    rx = None
    ry = None
    rz = None
    removed_cube_list = None

    def __init__(self, rx, ry, rz):
        assert rx[0] <= rx[1] and ry[0] <= ry[1] and rz[0] <= rz[1]
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.removed_cube_list = []

    def size_within_cube(self, cube):
        cube_intersection = self.get_intersection(cube)
        if cube_intersection is None:
            return 0
        size = cube_intersection.size()
        size -= sum([ r.size_within_cube(cube) for r in self.removed_cube_list ])
        return size

    def size(self):
        size = (self.rx[1] - self.rx[0] + 1) * (self.ry[1] - self.ry[0] + 1) * (self.rz[1] - self.rz[0] + 1)
        size -= sum([ r.size() for r in self.removed_cube_list ])
        return size

    def intersect(self, cube):
        if self.rx[0] > cube.rx[1] or self.rx[1] < cube.rx[0] \
                or self.ry[0] > cube.ry[1] or self.ry[1] < cube.ry[0] \
                or self.rz[0] > cube.rz[1] or self.rz[1] < cube.rz[0]:
            return False
        return True

    def get_intersection(self, cube):
        if not self.intersect(cube):
            return None
        return Cube((max(self.rx[0], cube.rx[0]), min(self.rx[1], cube.rx[1])),
                    (max(self.ry[0], cube.ry[0]), min(self.ry[1], cube.ry[1])),
                    (max(self.rz[0], cube.rz[0]), min(self.rz[1], cube.rz[1])))

    # Remove a section of the cube if it intersects with another cube.
    def remove(self, cube):
        cube_to_remove = self.get_intersection(cube)
        if cube_to_remove is not None:
            Cube.insert(self.removed_cube_list, cube_to_remove)

    @staticmethod
    # Insert a cube into a list by making sure it does not intersect with any other cube in that list.
    def insert(cube_list:list, cube):
        assert cube is not None
        for c in cube_list:
            c.remove(cube)
        cube_list.append(cube)

CUBE_LIST = []
for LINE in open(FILE):
    OP, COORD = LINE.strip().split(" ")
    X, Y, Z = COORD.split(",")
    RX = [int(x) for x in X[2:].split("..")]
    RY = [int(y) for y in Y[2:].split("..")]
    RZ = [int(z) for z in Z[2:].split("..")]
    if OP == 'on':
        Cube.insert(CUBE_LIST, Cube(RX, RY, RZ))
    else:
        SECTION_TO_REMOVE = Cube(RX, RY, RZ)
        for C in CUBE_LIST:
            C.remove(SECTION_TO_REMOVE)

LIMITED_DIM = (-50,50)
LIMITED_REGION = Cube(LIMITED_DIM, LIMITED_DIM, LIMITED_DIM)
NBR_OF_LIGHTS_ON_part1 = sum([C.size_within_cube(LIMITED_REGION) for C in CUBE_LIST])
print("part1: number lights on= {}".format(NBR_OF_LIGHTS_ON_part1))

NBR_OF_LIGHTS_ON_part2 = sum([C.size() for C in CUBE_LIST])
print("part2: number lights on= {}".format(NBR_OF_LIGHTS_ON_part2))

