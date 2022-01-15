import sys
import re
import numpy as np

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'


# Calculate the vector product of two vectors
def cross_product(a: list, b: list) -> list:
    assert len(a) == 3 and len(b) == 3

    c = list(range(3))
    c[0] = a[1] * b[2] - a[2] * b[1]
    c[1] = a[2] * b[0] - a[0] * b[2]
    c[2] = a[0] * b[1] - a[1] * b[0]
    return c


# Try a mapping 'm' for the two scanners indexes received
def try_mapping(m, s_index1, s_index2):
    m1 = m[s_index1]
    m2 = m[s_index2]
    s1 = S_LIST[s_index1]
    s2 = S_LIST[s_index2].copy()
    for i, b in enumerate(s2):
        s2[i] = np.dot(m2, b)

    # The prefix 'g_' is for coordinates in the global context (relative to scanner 0)
    for f1 in range(0, len(s1)):
        for f2 in range(len(s2)):
            g_fb1 = s1[f1]
            g_fb2 = s2[f2]
            g_pos2 = g_fb1 - g_fb2

            nb_matching_beacons = 0
            known_beacons1 = {}
            known_beacons2 = {}
            for i, b1 in enumerate(s1):
                # Check that there is enough beacons left to be able to reach the overlapping condition
                if nb_matching_beacons + (len(s1) - i) < 12:
                    break
                # Check if the beacon is in the range of the other scanner.
                g_s2_b1 = b1 - g_pos2
                within_range = (np.abs(g_s2_b1) <= 1000)
                if not within_range.all():
                    continue
                # The beacon should be visible to the second scanner
                tmp_nb_matching_beacons = nb_matching_beacons
                for j, b2 in enumerate(s2):
                    if i in known_beacons1:
                        break
                    if j in known_beacons2:
                        continue
                    g_tmp_b2 = b2 + g_pos2
                    if np.array_equal(b1, g_tmp_b2):
                        nb_matching_beacons += 1
                        known_beacons1[i] = j
                        known_beacons2[j] = i
                        if nb_matching_beacons >= 12:
                            return g_pos2
                # Skip checking the other beacons, since this one did not match
                # any beacons reported by the second scanner.
                if tmp_nb_matching_beacons == nb_matching_beacons:
                    break
    return None


def update_scanner_coord(index):
    global S_LIST
    s = S_LIST[index]
    g_pos = S_POS[index]
    for i, b in enumerate(s):
        s[i] = np.dot(S_ORIENT[index], b) + g_pos

NB_ITER = 0
def find_orientation():
    global S_LIST, S_ORIENT, S_POS, UNKNOWN_S, KNOWN_SCANNERS_TO_PROCESS, POSSIBLE_ORIENTATIONS, NB_ITER
    NB_ITER += 1
    for i in KNOWN_SCANNERS_TO_PROCESS.copy():
        for j in UNKNOWN_S.copy():
            # We are not expected more than 1, but ... who knows if the input is correct?
            found_possible_orientations = []
            for o in POSSIBLE_ORIENTATIONS:
                tmp_map = S_ORIENT.copy()
                tmp_map[j] = o
                print("scanner[{}] and scanner[{}]".format(i, j))
                pos = try_mapping(tmp_map, i, j)
                if pos is not None:
                    print("Found possible orientation: ", tmp_map[j])
                    print("pos[{}] = {}".format(j, pos))
                    found_possible_orientations.append((tmp_map, pos))
                    break
            if len(found_possible_orientations) > 1:
                print("OOps! We found {} possible orientations for scanner {}".format(len(
                    found_possible_orientations), j))
            elif len(found_possible_orientations) == 1:
                tmp_map, pos = found_possible_orientations[0]
                S_ORIENT = tmp_map
                S_POS[j] = pos
                UNKNOWN_S.remove(j)
                KNOWN_SCANNERS_TO_PROCESS.append(j)
                update_scanner_coord(j)
        KNOWN_SCANNERS_TO_PROCESS.remove(i)


def possible_orientations():
    o = []
    for i in range(6):
        for j in range(6):
            x = i % 3
            y = j % 3
            x_sign = -1 if i > 2 else 1
            y_sign = -1 if j > 2 else 1
            if x == y:
                continue

            a = []
            a.append([x_sign if x == i else 0 for i in range(3)])
            a.append([y_sign if y == i else 0 for i in range(3)])
            a.append(cross_product(a[0], a[1]))
            o.append(a[:])
    return o

def get_nb_beacons(scanner_list):
    uniq_beacons = {}
    for scanner in scanner_list:
        for beacon in scanner:
            get_hash = lambda b: b[0] + b[1] * 100000 + b[2] * 10000000000
            uniq_beacons[get_hash(beacon)] = np.array(beacon).tolist()
    uniq_beacons = sorted(uniq_beacons.values(), key=lambda x: x[0])
    # for beacon in uniq_beacon:
    #     print(beacon)
    print("Part1: nb of beacons = {}".format(len(uniq_beacons)))


# Known info
S_LIST = []
COORDS = []
for LINE in open(FILE):
    LINE = LINE.strip()
    if len(LINE) == 0:
        continue

    if re.match(r"--- scanner \d+.*", LINE):
        # print(LINE.split(" "))
        SCANNER_ID = LINE.split(" ")[2]
        if len(COORDS) > 0:
            S_LIST.append(COORDS)
        # print(COORDS)
        # Reset the COORDS (beacons list) for the next scanner
        COORDS = []
        continue
    COORDS.append([int(c) for c in LINE.split(",")])

if len(COORDS) > 0:
    S_LIST.append(COORDS)

print("nb of scanners:", len(S_LIST))
# print(S)

# Unknown at the beginning.
# Map of a scanner to a coordinate system (based on the first scanner). Each
# coord mapping has three lists, one mapping for each axis: x, y, z. The first
# scanner is assumed to be a direct mapping with [x,y,z].
S_ORIENT = {0: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}

# Position of each scanners relative to the first scanner (at index 0)
S_POS = {0: [0, 0, 0]}

# List of scanners that are not yet known in terms of position and mapping). At
# start, only scanner 0 is known as it is all relative to it.
UNKNOWN_S = list(range(1, len(S_LIST)))

# List of scanner that needs to be looked at.
KNOWN_SCANNERS_TO_PROCESS = [0]

POSSIBLE_ORIENTATIONS = possible_orientations()

while len(UNKNOWN_S) != 0:
    if len(KNOWN_SCANNERS_TO_PROCESS) == 0:
        break
    find_orientation()

if len(UNKNOWN_S) != 0:
    print("could not find info for scanners: {}".format(UNKNOWN_S))
else:
    get_nb_beacons(S_LIST)

MAX_DIST = 0


def get_distance(pos1, pos2):
    return np.sum(np.absolute(np.array(pos1) - np.array(pos2)))


for i in range(len(S_POS)):
    for j in range(i+1, len(S_POS)):
        TMP = get_distance(S_POS[i], S_POS[j])
        if TMP > MAX_DIST:
            MAX_DIST = TMP

print("part2: Max_distance = {}".format(MAX_DIST))
