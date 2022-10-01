with open('scratch_27.txt') as file_obj:
    file_data = file_obj.read()

file_data = file_data.split('\n')
results = list()
for row in file_data:
    data = row.split(' ')
    while '' in data:
        data.remove('')
    while '|' in data:
        data.remove('|')
    if data:
        results.append([int(num) for num in data])

output = list()
counter = 0
false_count = 0
for index, row in zip(range(1, len(results)), results):
    info = [num for num in row if num == index]
    print([num == index for num in row])
    if False in [num == index for num in row]:
        false_count += 1
    print(info)
    counter += 1

print(counter)
print(false_count)
