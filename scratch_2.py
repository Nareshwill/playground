import csv
import json
from pprint import pprint

# data = {'TV01': 0.0002342, 'TV02': 02342.2342, 'TV04': 0.34234}  # 0.0002342
# str_dict = str(data)
# print(str_dict)
# print(type(str_dict))
#
# casted_data = dict(data)
# print(casted_data)
# print(type(casted_data))
# for key in casted_data:
#     print(key, casted_data[key])

path = '/home/kpit/Downloads/level0_level1_kpi_1.csv'
csv_data = list(csv.DictReader(open(path)))

# tv_width = dict()
# for row in csv_data:
#     data = row['traffic_vehicle_width_half']
#     if data.startswith('{') and data.endswith('}'):
#         data = data.replace("'", '"')
#         casted_data = json.loads(data)
#         for key in casted_data:
#             if key not in tv_width:
#                 tv_width[key] = list()
#             tv_width[key].append(casted_data[key])
#             print("Key: {} & Value: {}".format(key, casted_data[key]))
#     else:
#         print(data)
#
#
# pprint(tv_width)


tv_width = list()
for row in csv_data:
    data = row['traffic_vehicle_width_half']
    if data.startswith('{') and data.endswith('}'):
        data = data.replace("'", '"')
        casted_data = json.loads(data)
        tv_width.append(casted_data)
    else:
        print(data)

pprint(tv_width)
with open('result.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=[key for key in tv_width[0].keys()])
    writer.writeheader()
    writer.writerows(tv_width)
