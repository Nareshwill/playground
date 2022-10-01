import io
import time
import logging
import traceback
import boto3
import pandas as pd

BUCKET_NAME = 'my-athena-scenario'
file_path = 'data/bench1/1620996313492/Reprocessed_Output/xosc_8e062586-1b26-4043-8b75-94c061b201bf/ground_truth_kpi.parquet'


def store(ground_truth_data):
    """
    RSS KPI: RSS Longitudinal safe distance
    Description:
    EV shall maintain minimum safe distance gap with longitudinal traffic
    Steps:
    1)Check for Longituinal Gap between EV and TV
    2)Evaluate for longitudinal Safe Gap between EV and TV
    3)if Longituinal Gap <longitunal Safe, RSS FLAG fail

    """
    csv_data = []

    try:
        logging.info(
            'Reading ground truth csv to generate "Rss Longitudinal safe check KPI"')
        # if Config.AWS_S3_ENABLED:
        #     s3_utils = S3Services()
        #     csv_reader = s3_utils.read_s3_csv_file(self.ground_truth_file)
        # else:
        #     if os.path.exists(self.ground_truth_file):
        #         csv_reader = list(csv.DictReader(open(self.ground_truth_file)))
        csv_reader = ground_truth_data['csv_data']
        for row in csv_reader:
            row_data = dict()
            row_data['timestamp'] = int(row["timestamp"])
            row_data['scenario_uuid'] = row["scenario_uuid"]
            row_data['date_id'] = row["date_id"]
            row_data['ad_start'] = row["ad_start"]

            if row['rss_long_current'] is not '':
                # pylint: disable=W0123
                row_data["rss_long_current"] = eval(
                    row['rss_long_current'])
                row_data["rss_long_safe"] = eval(row['rss_long_safe'])
                row_data["rss_long_flag"] = eval(row['rss_long_flag'])

                tv_id = list(row_data["rss_long_current"].keys())

                for target_iterator in range(len(tv_id)):
                    if row_data["rss_long_current"][tv_id[target_iterator]] > 100:
                        row_data["rss_long_current"][tv_id[target_iterator]] = 100.0
                        row_data["rss_long_safe"][tv_id[target_iterator]] = 0.0
                        row_data["rss_long_flag"][tv_id[target_iterator]] = 1

                if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                    overall_rss_flag = row["overall_rss_flag"]
                else:
                    overall_rss_flag = "True"
                row_data["overall_rss_flag"] = eval(overall_rss_flag)

                csv_data.append(row_data)
        logging.info(
            '"Rss longitudinal safe check KPI" report successfully generated')
    except Exception as e:
        logging.error('Error occurred ' + str(e))
        logging.error('Error occurred ' + traceback.format_exc())
        logging.error(
            '"Rss longitudinal safe check KPI" report failed to generated')
    return csv_data


def intermediate_evaluation(ground_truth_data):
    kpi_data = store(ground_truth_data)
    kpi_status = ""
    print(len([row.get('overall_rss_flag') for row in kpi_data if not row.get('overall_rss_flag')]))
    if len(kpi_data) > 0:
        if False not in [row.get('overall_rss_flag') for row in kpi_data]:
            kpi_status = "pass"
        else:
            kpi_status = "fail"
        logging.info(
            '"Rss longitudinal safe check KPI" status successfully generated as %s', kpi_status)
    return kpi_status


if __name__ == "__main__":
    start_time = time.time()
    s3_client = boto3.client('s3')
    s3_object = s3_client.get_object(
        Bucket=BUCKET_NAME,
        Key=file_path)
    file_data = io.BytesIO(s3_object['Body'].read())
    dataframe = pd.read_parquet(file_data)
    data = {
        "csv_data": dataframe.to_dict('records')
    }
    result = intermediate_evaluation(data)
    print(result)
    print(time.time() - start_time, 'seconds')
