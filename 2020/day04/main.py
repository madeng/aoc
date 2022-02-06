import sys
import re

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

F = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']

PL = []
P = {}
for I,LINE in enumerate(open(FILE)):
	LINE = LINE.strip()
	if LINE == '':
		PL.append(P)
		P = {}
		continue
	KV = [ t.split(':') for t in LINE.split() ]
	for K,V in KV:
		P[K] = V
PL.append(P)

VALID1 = 0
VALID2 = 0
for I,P in enumerate(PL):
	INVALID = False
	for K in F:
		if K == 'cid':
			continue
		if K not in P.keys():
			INVALID = True
	if INVALID == False:
		VALID1 += 1
	else:
		continue

	for K,V in P.items():
		if K == 'byr':
			if not 1920 <= int(V) <= 2002:
				INVALID = True
				break
		elif K == 'iyr':
			if not 2010 <= int(V) <= 2020:
				INVALID = True
				break
		elif K == 'eyr' :
			if not 2020 <= int(V) <= 2030:
				INVALID = True
				break
		elif K == 'hgt':
			TYP = V[len(V) - 2:]
			if TYP not in [ 'cm','in']:
				INVALID  =True
				break
			H = int(V[:len(V) - 2])
			if TYP == 'cm':
				if not 150<=H<=193:
					INVALID  =True
					break
			elif not 59 <= H <= 76:
				INVALID  =True
				break
		elif K == 'hcl':
			if V[0] != '#' :
				INVALID  =True
				break
			if not re.fullmatch(r'[a-z0-9]{6}',V[1:]):
				INVALID  =True
				break
		elif K == 'ecl':
			if V not in ['amb', 'blu','brn','gry','grn','hzl','oth']:
				INVALID  =True
				break
		elif K == "pid":
			if not re.fullmatch(r"\d{9}",V):
				INVALID  =True
				break

	if INVALID == False:
		VALID2 += 1

print('part1: valid=', VALID1)
print('part2: valid=', VALID2)
