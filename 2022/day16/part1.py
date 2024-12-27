import sys
import re

strip = lambda x : x.strip('\n')
LINES = list(map(strip, open(sys.argv[1] if len(sys.argv) > 1 else 'in').readlines()))
ANS = 0

DEBUG = True
def debug(*argv, **kwargs):
	if DEBUG == True:
		print(*argv, **kwargs)

def bfs(start_room, valve_rooms):
	global ROOM_GRAPH
	queue = [(0,start_room)]
	visited = [start_room]
	best_paths = {}
	tmp_valve_rooms = [v for v in valve_rooms]
	while len(tmp_valve_rooms) != 0 and len(queue) != 0:
		dist,room_name = queue.pop(0)
		_,neighbors = ROOM_GRAPH[room_name]
		if room_name in tmp_valve_rooms:
			best_paths[(start_room,room_name)] = dist
			tmp_valve_rooms.remove(room_name)
		if len(tmp_valve_rooms) == 0:
			break
		for n in neighbors:
			if n in visited:
				continue
			queue.append((dist+1,n))
		visited.append(room_name)
	if len(tmp_valve_rooms) != 0:
		print("not all room(s) have been found!")
	return best_paths

TIME_LIMIT = 30
ROOM_GRAPH = {}
VALVE_ROOMS = []
START = None
for l in LINES:
	src,rate,dest = re.search("alve (\w+) has flow rate=(\d+);.*to valves? (.*)", l).groups()
#	debug(src,rate,dest)
	if START is None:
		START = src
	dest = dest.replace(" ", '').split(",")
	ROOM_GRAPH[src] = (int(rate),dest)
	if int(rate) != 0:
		VALVE_ROOMS.append(src)

BEST = {}
TMP_VALVE_ROOMS = [n for n in VALVE_ROOMS]
#debug(TMP_VALVE_ROOMS)
if START not in TMP_VALVE_ROOMS:
	BEST |= bfs(START,TMP_VALVE_ROOMS)
for v in VALVE_ROOMS:
	BEST |= bfs(v, TMP_VALVE_ROOMS)
	TMP_VALVE_ROOMS.remove(v)
	if len(TMP_VALVE_ROOMS) <= 1:
		break

debug(BEST)

def search(start_room, minutes, current_rate, points, valve_rooms, path):
	debug("s={}, min={}, rate={}, pts={}, rooms={}, path={}".format(start_room, minutes, current_rate, points, valve_rooms, path))
	if minutes >= TIME_LIMIT:
		debug("# return points {} (after minutes={}), rate={}".format(points,minutes, current_rate))
		return {points:path}
	valve_rate = ROOM_GRAPH[start_room][0]
	if start_room in valve_rooms:
		# Try to open the valve in the current room
		debug("\nopening valve={}, at min={}, pts before={}, current_rate={}, valve_rate={}, new pts={}, new rate={}, new_minutes={}".format(start_room, minutes, points, current_rate, valve_rate, points+current_rate, current_rate+valve_rate, minutes+1))
		minutes += 1
		points += current_rate
		valve_rooms.remove(start_room)
		current_rate += valve_rate
	if len(valve_rooms) == 0:
		points += (TIME_LIMIT - minutes) * current_rate
		debug("### return points {}, rate={}, after minutes={}".format(points,current_rate, minutes))
		return {points:path}
	results = {}
	#debug("valve room :", valve_rooms)
	for v in valve_rooms:
		#debug('from {}, going to valve {}'.format(start_room, v))
		dist = BEST[(v,start_room)] if (v,start_room) in BEST else BEST[(start_room,v)]
		new_minutes = min(TIME_LIMIT, minutes + dist)
		new_points = points + (new_minutes - minutes) * current_rate
		valve_rooms_copy = [r for r in valve_rooms]
		result = search(v, new_minutes, current_rate, new_points, valve_rooms_copy, path + [v])
		results |= result

	return results

if sys.argv[1] == 'tin2':
	sys.exit(0)
if sys.argv[1] == 'tin':
	sys.exit(0)
#	test_valve_rooms = ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC']
#	test_points = search(START, minutes=0, current_rate=0, points=0, valve_rooms=test_valve_rooms, path=[START])
##	print('test::points', test_points)
#	best = max(test_points.keys())
#	print('points', best, test_points[best])
#elif sys.argv[1] == 'tin2':
#	test_points = search(START, minutes=0, current_rate=0, points=0, valve_rooms=VALVE_ROOMS, path=[START])
##	print('test::points', test_points)
#	best = max(test_points.keys())
#	print('points', best, test_points[best])
#else:
#	test_valve_rooms = ['OA', 'VP', 'VM', 'TR', 'DO', 'KI', 'HN', 'SH']
#	test_points = search(START, minutes=0, current_rate=0, points=0, valve_rooms=test_valve_rooms, path=[START])
#	print('test::points', test_points)
#
results = search(START, minutes=0, current_rate=0, points=0, valve_rooms=VALVE_ROOMS, path=[START])
print("results", results)
best = max(results.keys())
print('points', best, results[best],'\n\n\n\n\n\n\n\n\n\n\n\n')

#
if ANS != 0:
	print("ANSWER ==>  {}\n".format(ANS))
print('Done')
