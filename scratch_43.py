import pandas as pd

file_path = "/home/kpit/Downloads/ground_truth_kpi.parquet"
dataframe = pd.read_parquet(file_path)
data = dataframe.to_dict('records')
actual = [record.get('ego_acc_x') for record in data if record.get('ego_acc_x')]
print([record.get('ego_acc_x') for record in data])
print(len(actual))
print(len([record.get('ego_acc_x') for record in data]))


for column in dataframe.columns:
    print(column)
    # print(column, dataframe[column][0: 10])
    # print("rss_long_current", dataframe['rss_long_current'])
    # print("rss_long_safe", dataframe['rss_long_safe'])
    # print("rss_long_flag", dataframe['rss_long_flag'])
    # print("ad_start", dataframe['ad_start'])

print(dataframe['Server_response'][0:12])
print(dataframe['ego_acc_x'][0:12])
