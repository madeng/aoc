import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'in'

class File:
	def __init__(self, name, size):
		self.name = name
		self.size = size
		self.parent=None

	def getsize(self):
		return self.size

	def getlimitedsize(self,limit):
		return self.size

	def __eq__(self,other):
		if self.name == other.name:
			return True
		return False

	def __repr__(self):
		return self.name

	def getparent(self):
		if self.parent is None:
			return self
		return self.parent

class Dir(File):
	def __init__(self, name):
		self.files = []
		super().__init__(name, 0)

	def getsize(self):
		total=0
		for f in self.files:
			total+=f.getsize()
		return total

	def getlimitedsize(self,limit):
		global LSIZE
		total=0
		for f in self.files:
			total += f.getlimitedsize(limit)
		if total < limit:
			LSIZE += total
		return total


	def addfile(self, f):
		if f in self.files:
			print ("file was already in files:",f.name)
			return
		f.parent = self
		self.files.append(f)

	def getfile(self,name):
		for f in self.files:
			if f.name == name:
				return f
		return None


def parsecmd(l):
	global CUR
	l = l[2:]
	#print(' $ ',l)
	opts = l.split(' ')
	cmd = opts[0]
	if cmd == 'cd':
		tmp = CUR
		name = opts[1]
		if name == '/':
			CUR = ROOT
		elif name == '..':
			CUR = CUR.getparent()
		else:
			CUR = CUR.getfile(name)
		#print ("new CUR is {}, was {}".format(CUR, tmp))
	elif cmd == 'ls':
		pass

def parsecontent(l):
	global CUR
	size,name = l.split(' ')
	if size == 'dir':
		f = Dir(name)
	#	print("Add dir {} to cur {}".format(f, CUR))
	else:
		f = File(name,int(size))
#		print("Add dir {} to cur {}".format(f, CUR))
	CUR.addfile(f)

ANS = 0
ROOT = Dir("/")
CUR = ROOT
LSIZE = 0
for I, DLINE in enumerate(open(FILE)):
	L = DLINE.strip('\n')
	if L.startswith("$ "):
		parsecmd(L)
	else:
		parsecontent(L)

LIMIT = 100000
ANS = ROOT.getlimitedsize(LIMIT)
#print ("total used space = {}".format(ROOT.getsize()))
# 3688975 too high
print("ANSWER ==>  {}\n".format(LSIZE))
