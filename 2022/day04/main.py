import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

P1 = 0
P2 = 0

for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip()
	E1,E2 = L.split(",")
	X,Y = [int(i) for i in E1.split("-")]
	A,B = [int(i) for i in E2.split("-")]

	if (X >= A and Y <= B) or (A >= X and B <= Y):
		P1 += 1
		P2 += 1
	elif (X <= B and Y >= A) or (A <= Y and B >= X):
		P2 += 1

# 603 too high
# 584 is right
print("({}) Part 1 ==>  {}\n".format(FILE, P1))
print("({}) Part 2 ==>  {}\n".format(FILE, P2))
