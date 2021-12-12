import re

test_input_paths = ['testinput', 'testinput2', 'testinput3']
test_expected_results = [10, 19, 226]

input_path = 'input'
expected_result = None


# Return the list of possible paths to the end
def build_paths(node_map: dict, node_name: str, current_path: []):
    if re.match(r"[a-z]", node_name) and node_name in current_path:
        return None

    current_path.append(node_name)
    paths = []
    if node_name == 'end':
        paths.append(current_path)
    else:
        for n in node_map[node_name]:
            new_paths = build_paths(node_map, n, current_path.copy())
            if new_paths is not None and len(new_paths) != 0:
                paths.extend(new_paths)
    return paths


def part(file_path: str) -> int:
    with open(file_path) as input_file:
        m = {}
        line_list = [line.strip() for line in input_file]
        for rel in line_list:
            n1, n2 = rel.split("-")
            if n1 != 'end':
                m[n1] = [n2] if n1 not in m.keys() else [*m[n1], n2]
            if n2 != 'end':
                m[n2] = [n1] if n2 not in m.keys() else [*m[n2], n1]

    paths = build_paths(m, 'start', [])

    for p in paths:
        print(",".join(p))
    return len(paths)


def do_part_test() -> bool:
    is_success = True
    for index, file_path in enumerate(test_input_paths):
        result = part(file_path)
        test_expected_result = test_expected_results[index]
        if result != test_expected_result:
            print("Failure in test {}. Result is {}, expected {}".format(file_path, result, test_expected_result))
            is_success = False
            break
        else:
            print("Test success! Got {}, expected {}".format(result, test_expected_result))
        print('======================================================================')
    return is_success


def do_part():
    result = part(input_path)
    if expected_result is not None:
        if expected_result != result:
            print("wrong final result: {}".format(result))
        else:
            print("Correct final result: {}".format(result))
        return
    print("final result: {}".format(result))


if do_part_test():
    do_part()
