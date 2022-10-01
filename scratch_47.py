import io
import math
import time
import logging
import traceback
import boto3
import numpy as np
import pandas as pd

BUCKET_NAME = 'my-athena-scenario'
file_path = 'data/bench1/1620996313492/Reprocessed_Output/xosc_8e062586-1b26-4043-8b75-94c061b201bf/ground_truth_kpi.parquet'


def store(ground_truth_data):
    """
    Extracts longitudinal deceleration kpi data from carla ground truth kpi file
    Steps:
            1)Set no of samples= moving_average_time / sampling time
            2)Compute Acceleration moving average over samples
            3)Compute Longitudinal Jerk
            4)check if Longitudinal Jerk exceeds threshold at the Ego speeds as per table defined in Reference doc Inp2
    :return List()
    """
    csv_data = []
    LCA_flag_on = True
    jerk_data = list()

    try:
        logging.info(
            'Reading ground truth csv to generate "Level1 Longitudinal Jerk KPI"')
        # if os.path.exists(self.ground_truth_file):
        #     csv_reader = list(csv.DictReader(open(self.ground_truth_file)))
        #     ground_truth_data = pd.read_csv(self.ground_truth_file)
        # if Config.AWS_S3_ENABLED:
        #     s3_utils = S3Services()
        #     csv_reader = s3_utils.read_s3_csv_file(self.ground_truth_file)
        #     ground_truth_data = s3_utils.read_s3_csv_as_dataframe(self.ground_truth_file)
        # else:
        #     if os.path.exists(self.ground_truth_file):
        #         csv_reader = list(csv.DictReader(open(self.ground_truth_file)))
        #         ground_truth_data = pd.read_csv(self.ground_truth_file)

        csv_reader = ground_truth_data['csv_data']
        ground_truth_data = ground_truth_data['csv_df']

        output_kpi1_6 = pd.DataFrame()
        output_kpi1_6['timestamp'] = ground_truth_data['timestamp']
        output_kpi1_6['scenario_uuid'] = ground_truth_data['scenario_uuid']
        output_kpi1_6['date_id'] = ground_truth_data['date_id']
        output_kpi1_6['ad_start'] = ground_truth_data['ad_start']

        # Checking & Casting type
        if ground_truth_data['ego_velocity_x'].dtype == 'object':
            ground_truth_data['ego_velocity_x'] = ground_truth_data['ego_velocity_x'].astype(float)
        if ground_truth_data['ego_velocity_y'].dtype == 'object':
            ground_truth_data['ego_velocity_y'] = ground_truth_data['ego_velocity_y'].astype(float)
        if ground_truth_data['ego_acc_x'].dtype == 'object':
            ground_truth_data['ego_acc_x'] = ground_truth_data['ego_acc_x'].astype(float)
        if ground_truth_data['ego_acc_y'].dtype == 'object':
            ground_truth_data['ego_acc_y'] = ground_truth_data['ego_acc_y'].astype(float)

        output_kpi1_6['current_timestamp'] = ground_truth_data['current_timestamp']
        output_kpi1_6['ego_velocity_x'] = np.sqrt(
            ground_truth_data['ego_velocity_x'] ** 2 +
            ground_truth_data['ego_velocity_y'] ** 2)
        output_kpi1_6['ego_acc_x'] = np.sqrt(
            ground_truth_data['ego_acc_x'] ** 2 +
            ground_truth_data['ego_acc_y'] ** 2)
        output_kpi1_6['longitudinal_jerk'] = 0.00
        output_kpi1_6['kpi_pass_flag'] = True
        output_kpi1_6['lca_flag_on'] = True

        m_a_time_1006 = 1
        i = 0
        for row in csv_reader:
            row_data = dict()

            row_data['timestamp'] = int(row["timestamp"])
            row_data['scenario_uuid'] = row["scenario_uuid"]
            row_data['date_id'] = row["date_id"]
            row_data['ad_start'] = row["ad_start"]

            row_data['current_timestamp'] = float(row['current_timestamp'])
            if len(csv_data) > 0:
                sample_time = row_data['current_timestamp'] - \
                              csv_data[len(csv_data) - 1]['current_timestamp']
            else:
                sample_time = 0
            if sample_time != 0:
                samples = int(m_a_time_1006 / sample_time)
            else:
                samples = 1

            row_data['ego_velocity_x'] = math.sqrt(
                float(row["ego_velocity_x"]) ** 2 + float(row["ego_velocity_y"]) ** 2)
            row_data['ego_acc_x'] = math.sqrt(
                float(row["ego_acc_x"]) ** 2 + float(row["ego_acc_y"]) ** 2)

            accln_ma = [0]
            # 1 sec Moving average of Acceleration
            # i-1th sample
            if samples > i - 1 > 0:
                accln_ma[0] = output_kpi1_6['ego_acc_x'][0:i - 1].sum() / \
                              (i - 1)
            elif i - 1 > samples:
                accln_ma[0] = output_kpi1_6['ego_acc_x'][i - 1 - samples:i - 1].sum() / \
                              samples  # 81-1-20:81-1  60:80
            else:
                accln_ma[0] = output_kpi1_6['ego_acc_x'][0]

            # ith sample
            if samples > i > 0:
                accln_ma.append(output_kpi1_6['ego_acc_x'][0:i].sum() / i)
            elif i > samples:
                accln_ma.append(
                    output_kpi1_6['ego_acc_x'][i - samples:i].sum() / samples)
            else:
                accln_ma.append(output_kpi1_6['ego_acc_x'][0])

            # to avoid SettingWithCopyWarning.
            pd.options.mode.chained_assignment = None
            output_kpi1_6['longitudinal_jerk'][i -
                                               1] = float((accln_ma[1] - accln_ma[0]) / m_a_time_1006)

            print(len(output_kpi1_6['longitudinal_jerk'][0:i]), i)
            print("samples: ", samples, "sample_time: ", sample_time)
            if samples > i > 0:
                m_a_jerk = output_kpi1_6['longitudinal_jerk'][0:i].sum(
                ) / i
            elif i > samples:
                m_a_jerk = output_kpi1_6['longitudinal_jerk'][i -
                                                              samples:i].sum() / samples
            else:
                m_a_jerk = 0

            if output_kpi1_6['ego_velocity_x'][i] <= 5:
                if m_a_jerk > 5:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 5 < output_kpi1_6['ego_velocity_x'][i] <= 6:
                if m_a_jerk > 4.83:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 6 < output_kpi1_6['ego_velocity_x'][i] <= 7:
                if m_a_jerk > 4.67:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 7 < output_kpi1_6['ego_velocity_x'][i] <= 8:
                if m_a_jerk > 4.5:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 8 < output_kpi1_6['ego_velocity_x'][i] <= 9:
                if m_a_jerk > 4.33:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 9 < output_kpi1_6['ego_velocity_x'][i] <= 10:
                if m_a_jerk > 4.17:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 10 < output_kpi1_6['ego_velocity_x'][i] <= 11:
                if m_a_jerk > 4:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 11 < output_kpi1_6['ego_velocity_x'][i] <= 12:
                if m_a_jerk > 3.83:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 12 < output_kpi1_6['ego_velocity_x'][i] <= 13:
                if m_a_jerk > 3.67:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 13 < output_kpi1_6['ego_velocity_x'][i] <= 14:
                if m_a_jerk > 3.5:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 14 < output_kpi1_6['ego_velocity_x'][i] <= 15:
                if m_a_jerk > 3.33:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 15 < output_kpi1_6['ego_velocity_x'][i] <= 16:
                if m_a_jerk > 3.17:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 16 < output_kpi1_6['ego_velocity_x'][i] <= 17:
                if m_a_jerk > 3:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 17 < output_kpi1_6['ego_velocity_x'][i] <= 18:
                if m_a_jerk > 2.83:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            elif 18 < output_kpi1_6['ego_velocity_x'][i] <= 19:
                if m_a_jerk > 2.67:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False
            else:
                if m_a_jerk > 2.5:
                    if row["ad_start"] == '1' or row["ad_start"] == '1.0':
                        output_kpi1_6['kpi_pass_flag'][i] = False

            row_data['KPI_pass_Flag'] = bool(
                output_kpi1_6['kpi_pass_flag'][i])
            row_data['LCA_flag_on'] = LCA_flag_on
            i = i + 1

            csv_data.append(row_data)

            longitudinal_jerk_lst = output_kpi1_6['longitudinal_jerk'].tolist(
            )
            longitudinal_jerk = [str(x) for x in longitudinal_jerk_lst]

            jerk_data = list()
            for row_data, jerk in zip(csv_data, longitudinal_jerk):
                row_data['longitudinal_jerk'] = jerk
                jerk_data.append(row_data)
            # print("The jerk value", longitudinal_jerk)
        logging.info(
            '"Level1 Longitudinal Jerk KPI" report successfully generated')
    except Exception as e:
        logging.error('Error occurred ' + str(e))
        logging.error('Error occurred ' + traceback.format_exc())
        logging.error(
            '"Level1 Longitudinal Jerk KPI" report failed to generated')

    return jerk_data


def intermediate_evaluation(ground_truth_data):
    kpi_data = store(ground_truth_data)
    kpi_status = True
    if len(kpi_data) > 0:
        if False not in [row.get('KPI_pass_Flag') for row in kpi_data]:
            kpi_status = "pass"
        else:
            kpi_status = "fail"
        logging.info(
            '"Level1 Longitudinal Jerk KPI" status successfully generated as %s', kpi_status)
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
        "csv_data": dataframe.to_dict('records'),
        "csv_df": dataframe
    }
    result = intermediate_evaluation(data)
    print(result)
    print(time.time() - start_time, 'seconds')
