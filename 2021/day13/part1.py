
test_input_paths = ['testinput']
test_expected_results = [17]
expected_result = None

input_path = 'input'

max_x = max_y = -1


def apply_op(op, grid):
    global max_x, max_y
    axis,index = op.split('=')
    index = int(index)
    start_x = index + 1 if axis == 'x' else 0
    start_y = index + 1 if axis == 'y' else 0
    for y in range(start_y, max_y + 1):
        for x in range(start_x, max_x + 1):
            if not grid[y][x]:
                continue
            if axis == 'x':
                grid[y][2*index - x] = True
            else:
                grid[2*index - y][x] = True
    if axis == "x":
        max_x = index - 1
    else:
        max_y = index - 1


def part(file_path: str) -> int:
    global max_x, max_y
    map = []
    with open(file_path) as input_file:
        line_list = [line.strip() for line in input_file]

    is_coord_section = True
    op_list = []
    for line in line_list:
        if line == '':
            is_coord_section = False
            continue
        if is_coord_section:
            x, y = [int(c) for c in line.split(',', )]
            map.append((x,y))
            max_x = max(x, max_x)
            max_y = max(y, max_y)
        else:
            op_list.append(line.split(" ")[2])

    grid = [[False for x in range(max_x + 1)] for y in range(max_y + 1)]
    for x, y in map:
        grid[y][x] = True

    apply_op(op_list[0], grid)

    nb_dots = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            nb_dots += 1 if grid[y][x] else 0

    return nb_dots


def do_part_test() -> bool:
    is_success = True
    for index,file_path in enumerate(test_input_paths):
        result = part(file_path)
        test_expected_result = test_expected_results[index]
        if result != test_expected_result:
            print("1-Failure in test {}. Result is {}, expected {}".format(file_path, result, test_expected_result))
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

