from pprint import pprint
file_name = 'scratch_20.txt'


def read_txt_file(file_path):
    with open(file_path) as file_obj:
        data = file_obj.read()
    return data


file_data = read_txt_file(file_path=file_name)
file_data = file_data.split('\n')

result = list()
diff = list()
for line in file_data:
    if '-' in line or 'scene_id' in line:
        continue
    info = [row for row in line.replace(' ', '').split('|') if row]
    if info:
        text = "{}, scene_id: {}, scenario_id: {}, session_id: {}".format(
            info[0] == info[1],
            info[0],
            info[1],
            info[2]
        )
        result.append(text)
        if not info[0] == info[1]:
            diff.append(text)

file_info = '\n'.join(result)
with open('local.txt', mode='w') as file_ob:
    file_ob.write(file_info)

pprint(diff)

# print("#"*12, "Oregon", "#"*12)
# oregon = read_txt_file(file_path='oregon.txt')
# diff = list()
# for line in oregon.split('\n'):
#     if line.startswith('False'):
#         diff.append(line)
#
# pprint(diff)