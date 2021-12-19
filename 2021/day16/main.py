import sys
from functools import reduce

infile = sys.argv[1] if len(sys.argv)>1 else '16.in'

def get_bin(hex: str) -> str:
    return bin(int(hex, 16))[2:].zfill(len(hex) * 4)

def get_lit_val(p):
    v = 0
    while p[0] != '0':
        v = v << 4 | int(p[1:5],2)
        p = p[5:]

    v = v << 4 | int(p[1:5],2)
    return (p[5:], v)

def read_packet(p):
    pv = int(p[0:2+1],2)
    pt = int(p[3:5+1],2)

    sum_pv = pv
    if pt == 4:
        p, pval = get_lit_val(p[6:])
    else:
        # operator packet
        sub_bit_length = 1e9
        nb_sub_p = 1e9
        if p[6] == '0':
            # Length type ID == 0
            sub_bit_length = int(p[7:21+1],2)
            p = p[22:]
        else:
            # Length type ID == 1
            nb_sub_p = int(p[7:17+1],2)
            p = p[18:]

        sub_p_count = 0
        bits_read = 0
        sub_pval_list = []
        while sub_p_count < nb_sub_p and bits_read < sub_bit_length - 3:
            sub_p_count += 1
            len_b = len(p)

            sum_subp_v, sub_pval, p = read_packet(p)
            sub_pval_list.append(sub_pval)

            sum_pv += sum_subp_v
            bits_read += len_b - len(p)

        pval = 0
        if pt == 0:
           pval = sum(sub_pval_list)
        elif pt == 1:
            pval = reduce(lambda x,y:x*y, sub_pval_list)
        elif pt == 2:
            pval = min(sub_pval_list)
        elif pt == 3:
            pval = max(sub_pval_list)
        elif pt == 5:
            pval = 1 if sub_pval_list[0] > sub_pval_list[1] else 0
        elif pt == 6:
            pval = 1 if sub_pval_list[0] < sub_pval_list[1] else 0
        elif pt == 7:
            pval = 1 if sub_pval_list[0] == sub_pval_list[1] else 0

    return (sum_pv, pval, p)

for line in open(infile):
    bin = get_bin(line.strip())
    sum_pv, pval, p = read_packet(bin)
    print("part1 - sum_pv = {}".format(sum_pv))
    print("part2 - pval = {}".format(pval))

