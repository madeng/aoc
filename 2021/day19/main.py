import sys
import re

file = sys.argv[1] if len(sys.argv)>1 else 't1in'

def try_mapping(m, s1, s2):
	
	
# Unknown at the beginning. 
# Map of a scanner to a coordinate system (based on the first scanner). Each coord mapping has three elements, one for each axis: x, y, z
MAP = {}
# Position of each scanners relative to the first scanner
SCANNERS_POS = {}

# Known info
SCANNERS = []
coords = []
for line in open(file):
	line = line.strip()
	if len(line) == 0:
		continue

	if re.match(r"--- scanner \d+.*", line):
		print(line.split(" "))
		SCANNER_ID = line.split(" ")[2]
		if len(coords) > 0:
			SCANNERS.append(coords)
			print(coords)
		# Reset the coords (beacons list) for the next scanner
		coords = []
		continue
	coords.append([int(c) for c in line.split(",")])

if len(coords) > 0:
	SCANNERS.append(coords)

print("nb of scanners:", len(SCANNERS))
print(SCANNERS)
 