# Example
#test_input_paths = ['testinput', 'testinput2', 'testinput3']
test_input_paths = ['testinput']
test_expected_results = [0]

input_path = 'input'
expected_result = None


def part(file_path: str) -> int:
    with open(file_path) as input_file:
        for line in [line.strip() for line in input_file]:
            pass

    return 0


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
