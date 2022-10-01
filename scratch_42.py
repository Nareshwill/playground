def even(start, n):
    end = 2
    if start % 2 != 0:
        end = 3
        start = start + 1
    return [i for i in range(start, (n + n + end), 2) if i % 2 == 0]


if __name__ == "__main__":

    print(even(5, 7))

    text = "queen she she the was was"
    words = text.split(" ")
    occurrences = dict()
    for char in words:
        if char not in occurrences:
            occurrences[char] = 0
        occurrences[char] += 1

    value = sorted(occurrences.keys())
    print([occurrences[data] for data in value])

    fruits = ['apple', 'banana', 'orange']


    def is_a_fruit(item):
        return item in fruits


    # def
    # t = [9, 4, 3, 6, 7]
    #
    # result = t.index(value)
    # if value % 2 == 0:
    #     return True
    # return False

    def fizz_buzz():
        pass
