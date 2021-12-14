# Example
#test_input_paths = ['testinput', 'testinput2', 'testinput3']
test_input_paths = ['testinput']
test_expected_results = [2188189693529]

input_path = 'input'
expected_result = None


def step(pairs:{}, pair_occurrences:{}) -> dict:
    new_pair_occur = {}
    for s,nb_s in pair_occurrences.items():
        new_pair1 = s[0] + pairs[s]
        new_pair2 = pairs[s] + s[1]
        o = pair_occurrences[s]
        new_pair_occur[new_pair1] = o if new_pair1 not in new_pair_occur.keys() else new_pair_occur[new_pair1] + o
        new_pair_occur[new_pair2] = o if new_pair2 not in new_pair_occur.keys() else new_pair_occur[new_pair2] + o
    return new_pair_occur


def part(file_path: str) -> int:
    with open(file_path) as input_file:
        is_polymer_tmpl = True
        tmpl = ''
        first_char_in_tmpl = None
        pairs_mapping = {}
        pair_occur_in_tmpl = {}
        for line in [line.strip() for line in input_file]:
            if line == '':
                is_polymer_tmpl = False
                continue
            if is_polymer_tmpl:
                for i in range(len(line)-1):
                    pair = line[i:i + 2]
                    pair_occur_in_tmpl[pair] = 1 if pair not in pair_occur_in_tmpl.keys() else pair_occur_in_tmpl[pair] + 1
                    if first_char_in_tmpl is None:
                        first_char_in_tmpl = line[i]
            else:
                o, t = line.split(' -> ')
                pairs_mapping[o] = t

        steps = 40
        for s in range(steps):
            pair_occur_in_tmpl = step(pairs_mapping, pair_occur_in_tmpl)

        char_occurs={}
        for pair,nb_occur in pair_occur_in_tmpl.items():
            char_occurs[pair[1]] = nb_occur if pair[1] not in char_occurs.keys() else char_occurs[pair[1]] + nb_occur

        if first_char_in_tmpl not in pair_occur_in_tmpl:
            pair_occur_in_tmpl[first_char_in_tmpl] = 1
        else:
            pair_occur_in_tmpl[first_char_in_tmpl] += 1

        min = None
        max = None
        for nb_occur in char_occurs.values():
            min = nb_occur if min is None or min > nb_occur  else min
            max = nb_occur if max is None or max < nb_occur else max
        print("most common: ", max)
        print("least common: ", min)
        print("diff = ", max - min)

    return max - min


def do_part_test( ) -> bool:
    is_success =True
    for index,  file_path in enumerate(test_input_paths):
        result = part(file_path)
        test_expected_result = test_expected_results[index]
        if result != test_expected_result:
            print("1-Failure in test {}. Result is {}, expected {}".format(test_input_paths, result, test_expected_result))
            is_success = False
        else:
            print("1-Test success! Got {}, expected {}".format(result, test_expected_result))
    return is_success

def do_part():
    result = part(input_path)
    if expected_result is not None:
        if expected_result != result:
            print("1-wrong final result: {}".format(result))
        else:
            print("1-Correct final result: {}".format(result))
        return
    print("1-final result: {}".format(result))


if do_part_test():
    do_part()
