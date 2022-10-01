def compare_components(input_list, temp_data):
    input_set = set(input_list)
    temp_set = set(temp_data)
    common_set = input_set.intersection(temp_set)
    return common_set


def test_compare_components():
    result = compare_components([1, 2, 3], [2, 3, 4])
    result = list(result)
    assert result[0] == 2
    assert result[1] == 3


if __name__ == "__main__":
    result = compare_components([1, 2, 3], [2, 3, 4])
    result = list(result)
    assert result[0] == 2
    assert result[1] == 3
    print(result)
