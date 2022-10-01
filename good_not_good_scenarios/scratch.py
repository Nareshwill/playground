import json
from pprint import pprint

json_file_path = '/home/kpit/miscellaneous_code/validation-checks/server/base_scenario_and_variations.json'
with open(json_file_path) as json_file:
    data = json.load(json_file)

info = data[0]
result = dict()
result['total_base_scenarios'] = len(info['base_scenario_info'])
result['total_good_base_scenarios'] = 0
result['total_good_variations'] = 0
result['total_variations'] = 0

for base_scenario_info in info['base_scenario_info']:
    total_variations = len(base_scenario_info.get('variations'))
    total_passed_variations = len([doc for doc in base_scenario_info.get('variations') if doc.get('failed') == 0])
    if total_variations == total_passed_variations:
        result['total_good_base_scenarios'] += 1
        result['total_good_variations'] += total_variations
        print(base_scenario_info['base_scenario_name'])
    else:
        result
    result['total_variations'] += total_variations

result['total_not_good_base_scenarios'] = result['total_base_scenarios'] - result['total_good_base_scenarios']
result['total_not_good_variations'] = result['total_variations'] - result['total_good_variations']

pprint(result)
