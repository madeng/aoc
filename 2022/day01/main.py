import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

TOTAL_PER_ELF=[]
MAXIMUM=0
SUM=0
for DLINE in open(FILE):
	LINE = DLINE.strip()
	if LINE == '':
		if SUM > MAXIMUM:
			MAXIMUM = SUM
		TOTAL_PER_ELF.append(SUM)
		SUM = 0
	else:
		SUM += int(LINE)
if SUM > 0:
	TOTAL_PER_ELF.append(SUM)
	if SUM > MAXIMUM:
		MAXIMUM = SUM

#print(str(TOTAL_PER_ELF))
print("1- top = {}".format(MAXIMUM))

TOTAL_PER_ELF.sort()
TOP3 = sum(TOTAL_PER_ELF[-3:])
print("2- top3 = {}".format(TOP3))

