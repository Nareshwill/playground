import os
import csv
import pyarrow.csv as pv
import pyarrow.parquet as pq
import time
import boto3
import io
import pandas as pd
from pprint import pprint




# l0 = time.time()
# parquet_file = '/home/kpit/Downloads/rss_kpi.parquet'
# parquet_file = '/home/kpit/Downloads/level0_level1_kpi.parquet'
# df = pd.read_parquet(parquet_file)
# data = df.to_dict('records')
# print(len(data))
# pprint(data[0])
# print("Total time taken: ", time.time() - l0)

# csv_file = '/home/kpit/Downloads/gt_files_20220204_155632/gt_files/rss_kpi.csv'
# csv_data = list(csv.DictReader(open(csv_file)))
# pprint(csv_data[0])

# s3_client = boto3.client('s3')
# s3_object = s3_client.get_object(Bucket='cclp-bench-data-dev-01', Key='data/bench1/1643970951925-65ebba47-ecc3-47f8-8757-051725702dd4/Reprocessed_Output/xosc_a6a881cb-ab66-48c9-b17c-9aba24113629/rss_kpi.parquet')
# dataframe = pd.read_parquet(io.BytesIO(s3_object['Body'].read()))
# pprint(dataframe.to_dict('records')[0])

# key = "level0_level1_kpi.parquet"
# # memory_file = io.BytesIO()
# # dataframe = pd.read_parquet(parquet_file)
# # dataframe.to_parquet(memory_file, index=False)
# #
# s3_client = boto3.client('s3')
# # s3_client.put_object(Bucket='cclp-bench-data-dev-01', Key=key, Body=memory_file.getvalue())
#
# s3_object = s3_client.get_object(Bucket='cclp-bench-data-dev-01', Key=key)
# dataframe = pd.read_parquet(io.BytesIO(s3_object['Body'].read()))
# print(dataframe)
# print(len(dataframe.to_dict('records')))
# print("Total timetaken (s)", time.time() - l0)

def upload_kpi_file_in_parquet_format():
    t0 = time.time()
    key = os.path.join("data",
                       "bench1",
                       "1643970951925-65ebba47-ecc3-47f8-8757-051725702dd4",
                       "Reprocessed_Output",
                       "xosc_a6a881cb-ab66-48c9-b17c-9aba24113629")
    path = "/home/kpit/Downloads/gt_files_20220204_155632/gt_files"
    s3_client = boto3.client('s3')
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_data = list(csv.DictReader(open(os.path.join(path, file))))
            dataframe = pd.DataFrame.from_dict(file_data, orient='columns')
            memory_file = io.BytesIO()
            dataframe.to_parquet(memory_file, index=False)
            s3_client.put_object(Bucket='cclp-bench-data-dev-01',
                                 Key=os.path.join(key, file.replace('csv', 'parquet')),
                                 Body=memory_file.getvalue())
            print(os.path.join(key, file.replace('csv', 'parquet')))
    print("Total timetaken (s):", time.time() - t0)


def upload_kpi_file_in_csv_format():
    t0 = time.time()
    key = os.path.join("data",
                       "bench1",
                       "1644066519697-905f4ff1-9a26-4b37-9c9e-f8180703f185",
                       "Reprocessed_Output",
                       "xosc_155d29b8-ac7b-46bf-8762-5495dfb4c784")
    path = "/home/kpit/Downloads/gt_files_20220204_155632/gt_files"
    s3_resource = boto3.resource('s3')
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_data = list(csv.DictReader(open(os.path.join(path, file))))
            memory_file = io.StringIO()
            writer = csv.DictWriter(memory_file, fieldnames=[key for key in file_data[0].keys()])
            writer.writeheader()
            writer.writerows(file_data)
            s3_resource.Object("cclp-migration-data-test-02", os.path.join(key, file)).put(Body=memory_file.getvalue())
            print(os.path.join(key, file))
    print("Total time taken", time.time() - t0)


# s3_client = boto3.client('s3')
# response = s3_client.list_objects_v2(Bucket='cclp-bench-data-dev-01', Prefix='data/bench1/1631098174959-61732184-bbb2-41de-ad57-9cb57dceddae/Reprocessed_Output')
# # print(response)
# for obj in response['Contents']:
#     print(obj)
#     print(obj['Key'])

# print("")

def convert_csv_to_parquet():
    l0 = time.time()
    gt_file_path = "/home/kpit/Downloads/parquet_examine/gt_files_20220209_193218/gt_files"
    target_directory = os.path.join(gt_file_path, 'parquet')
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    for filename in os.listdir(gt_file_path):
        if os.path.isfile(os.path.join(gt_file_path, filename)):
            table = pv.read_csv(os.path.join(gt_file_path, filename))
            pq.write_table(table, os.path.join(target_directory, filename.replace('csv', 'parquet')))
    kpi_file_path = '/home/kpit/Downloads/parquet_examine/kpi_files_20220209_193235/kpi_files'
    kpi_directory = os.path.join(kpi_file_path, 'parquet')
    if not os.path.exists(kpi_directory):
        os.makedirs(kpi_directory)
    for filename in os.listdir(kpi_file_path):
        print(filename)
        if os.path.isfile(os.path.join(kpi_file_path, filename)):
            table = pv.read_csv(os.path.join(kpi_file_path, filename))
            pq.write_table(table, os.path.join(kpi_directory, filename.replace('csv', 'parquet')))
    print("Total time taken :", time.time() - l0)


if __name__ == "__main__":
    # upload_kpi_file_in_parquet_format()
    # upload_kpi_file_in_csv_format()
    convert_csv_to_parquet()
    pass
