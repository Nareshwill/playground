import io
import os
import time
import zipfile
import json
import base64
import zlib
from io import BytesIO

import yaml
import boto3
import pandas as pd
from smart_open import open as sm_open
from flask import Flask, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)


@app.route('/create_yaml')
def create_yaml_file():
    data = {
        'a': ['contains', 'something'],
    }
    memory_file = BytesIO()
    memory_file.write(bytes(yaml.dump(data=data, default_flow_style=False), 'utf-8'))
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, attachment_filename='file.yaml')


def get_files_present(s3_client, prefix, bucket_name='cclp-bench-data-dev-01'):
    files_present = list()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = response.get('Contents')
    for file_info in files:
        file_path = file_info.get('Key')
        file_name = os.path.basename(file_path)
        files_present.append(file_name)
    return files_present


def read_file_as_bytes(path, bucket_name='cclp-bench-data-dev-01'):
    file_path = os.path.join('s3://', bucket_name, path)
    with sm_open(file_path, mode='rb') as s3_file:
        file_data = s3_file.read()
    return file_data


def read_parquet_file(s3_client, path, bucket_name='cclp-bench-data-dev-01'):
    print(path)
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=path)
    file_data = io.BytesIO(s3_object['Body'].read())
    dataframe = pd.read_parquet(file_data)
    data = dataframe.to_dict('records')
    return base64.b64encode(zlib.compress(str.encode(json.dumps(data), 'utf-8'), 6))


@app.route('/download/files', methods=['POST'])
def download_files():
    s3_client = boto3.client('s3')
    files = ['ground_truth_kpi.parquet', 'rss_kpi.parquet', 'level0_level1_kpi.parquet']
    key = os.path.join('data',
                       'bench1',
                       '1631098174959-61732184-bbb2-41de-ad57-9cb57dceddae',
                       'Reprocessed_Output',
                       'xosc_61732184-bbb2-41de-ad57-9cb57dceddae')
    files_present = get_files_present(s3_client=s3_client, prefix=key)
    memory_file = io.BytesIO()
    with zipfile.ZipFile(
        memory_file,
        mode='w'
    ) as z_file:
        for filename in files:
            if filename in files_present:
                path = os.path.join(key, filename)
                zip_info = zipfile.ZipInfo(os.path.join('gt_files', filename.replace('parquet', 'csv')))
                zip_info.date_time = time.localtime(time.time())[:6]
                zip_info.compress_type = zipfile.ZIP_DEFLATED
                file_data = read_parquet_file(s3_client=s3_client, path=path)
                z_file.writestr(zip_info, file_data)
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True,
                     mimetype='application/zip', attachment_filename='gt.zip')


@app.route('/index')
def index():
    return render_template('scratch_23.html')


if __name__ == '__main__':
    app.run()
