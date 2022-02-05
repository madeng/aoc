import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else 'day25/tin'


def print_map(map_):
    print("  0123456789")
    for i,x in enumerate(map_):
        print(f"{i} ", end='')
        for j,c in enumerate(x):
            if c == None:
                print('.',end='')
                continue
            print(c,end='')
        print()

M = []
for LINE in open(FILE):
    S = LINE.strip()
    M.append([None if c == '.' else c for c in S])

print_map(M)

assert(len(M) > 0)
assert(len(M[0]) > 0)

COUNT = 0
MOVE = True
while MOVE:
    MOVE = False
    JM = False  # Just moved
    ZM = False  # Cucumber at index 0 has moved
    # Horizontal moves
    for I,X in enumerate(M):
        ZM = False
        JM = False
        for J,C in enumerate(X):
            if JM == True:
                JM = False
                continue
            if J == len(X) - 1 and ZM == True:
                ZM = False
                continue
            if C != '>':
                continue
            N = J + 1 if J < len(X) - 1 else 0
            if X[N] == None:
                X[N] = C
                X[J] = None
                MOVE = True
                if J == 0:
                    ZM = True
                JM = True
   # print("After horizontal moves...")
   # print_map(M)

    # Vertical moves
    for J in range(len(M[0])):
        ZM = False
        JM = False
        for I in range(len(M)):
            if JM == True:
                JM = False
                continue
            if I == len(M) - 1 and ZM == True:
                ZM = False
                continue
            C = M[I][J]
            if C != 'v':
                continue
            N = I + 1 if I < len(M) - 1 else 0
            if M[N][J] == None:
                M[N][J] = C
                M[I][J] = None
                JM = True
                if I == 0:
                    ZM = True
                MOVE = True
    COUNT += 1
    #print(f"\nAfter {COUNT} steps")
    #print_map(M)

print(f"Could not move after {COUNT} steps")
