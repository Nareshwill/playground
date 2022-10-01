# import json
# from pprint import pprint
#
# mumbai_path = '/home/kpit/miscellaneous_code/gt_file_info/mumbai/output.json'
# oregon_path = '/home/kpit/miscellaneous_code/gt_file_info/oregon/output.json'
# virginia_path = '/home/kpit/miscellaneous_code/gt_file_info/virginia/output.json'
#
#
# def read_json(path):
#     with open(path) as json_file:
#         data = json.load(json_file)
#     return data
#
#
# result = list()
# paths = [mumbai_path, oregon_path, virginia_path]
# for file_path in paths:
#     result.extend(read_json(path=file_path))
#
# out_paths = list()
# for info in result:
#     out_paths.append("data/bench1/{}/{}".format(info['test_run_id'], info['scenario_uuid']))
#
# pprint(out_paths)
# print(len(out_paths))

# import zipfile
#
# with zipfile.ZipFile('sample.zip', 'w', zipfile.ZIP_DEFLATED) as zip_obj:
#     zip_obj.writestr("data/file.txt", 'Hwllo World!')

def get_result(tp, fp, fn):
    if int(tp) > (int(fp) + int(fn)):
        result = 'PASS'
        remark = ''
        return result, remark
    else:
        result = 'FAIL'
        remark = "TP is less than FP + FN"
        return result, remark
