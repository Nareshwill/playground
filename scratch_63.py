import csv
import json
import ast

file_path = '/home/kpit/Downloads/logs-insights-results (6).csv'

# with open(file_path) as csv_file:
#     data = csv.DictReader(csv_file)

data = list(csv.DictReader(open(file_path)))

for row in data:
    message = row.get('@message')
    # print(type(message))
    # print(message)
    # event = ast.literal_eval(message)
    if message.startswith('1: '):
        if len(message) > 2111:
            print(len(message))
            print(message)
