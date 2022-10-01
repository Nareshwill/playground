# Check Longitudinal Deceleration.
import csv
import pandas as pd
import numpy as np

file_path = '/home/kpit/execution/ground_truth_kpi.parquet'


def check_longitudinal_deceleration():
    ground_truth_data = pd.read_parquet(file_path)

    # Extracting l1_longitudinal_deceleration_kpi KPI
    LCA_flag_on = True

    output_df = pd.DataFrame()
    output_df['timestamp'] = ground_truth_data["timestamp"]
    output_df['scenario_uuid'] = ground_truth_data["scenario_uuid"]
    output_df['date_id'] = ground_truth_data["date_id"]
    output_df['ad_start'] = ground_truth_data["ad_start"]
    output_df['current_timestamp'] = ground_truth_data["current_timestamp"]

    output_df['ego_velocity_x'] = np.sqrt(
        ground_truth_data["ego_velocity_x"] ** 2 + ground_truth_data["ego_velocity_y"] ** 2)
    output_df['ego_acc_x'] = np.sqrt(
        ground_truth_data["ego_acc_x"] ** 2 + ground_truth_data["ego_acc_y"] ** 2)

    temp_df = pd.DataFrame()
    temp_df['timestamp'] = ground_truth_data["timestamp"]
    temp_df['KPI pass Flag'] = True

    ego_acc_x_list = list()
    kpi_pass_flag_list = list()
    m_a_time_1004 = 2
    for i in range(len(output_df['current_timestamp'])):
        if len(ego_acc_x_list) > 0:
            sample_time = output_df['current_timestamp'][i] - output_df['current_timestamp'][i - 1]
        else:
            sample_time = 0

        if sample_time != 0:
            samples = int(m_a_time_1004 / sample_time)
        else:
            samples = 1

        if samples > i > 0:
            m_a_accln = output_df['ego_acc_x'][0:i].sum() / i
        elif i > samples:
            m_a_accln = output_df['ego_acc_x'][i - samples:i].sum() / samples
        else:
            m_a_accln = output_df['ego_acc_x'][0]
        ego_acc_x_list.append(m_a_accln)

        if output_df['ego_velocity_x'][i] <= 5:
            if m_a_accln > 5:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 5 < output_df['ego_velocity_x'][i] <= 6:
            if m_a_accln > 4.87:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 6 < output_df['ego_velocity_x'][i] <= 7:
            if m_a_accln > 4.73:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 7 < output_df['ego_velocity_x'][i] <= 8:
            if m_a_accln > 4.6:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 8 < output_df['ego_velocity_x'][i] <= 9:
            if m_a_accln > 4.47:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 9 < output_df['ego_velocity_x'][i] <= 10:
            if m_a_accln > 4.33:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 10 < output_df['ego_velocity_x'][i] <= 11:
            if m_a_accln > 4.2:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 11 < output_df['ego_velocity_x'][i] <= 12:
            if m_a_accln > 4.07:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 12 < output_df['ego_velocity_x'][i] <= 13:
            if m_a_accln > 3.93:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 13 < output_df['ego_velocity_x'][i] <= 14:
            if m_a_accln > 3.8:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 14 < output_df['ego_velocity_x'][i] <= 15:
            if m_a_accln > 3.67:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 15 < output_df['ego_velocity_x'][i] <= 16:
            if m_a_accln > 3.53:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 16 < output_df['ego_velocity_x'][i] <= 17:
            if m_a_accln > 3.4:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 17 < output_df['ego_velocity_x'][i] <= 18:
            if m_a_accln > 3.27:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        elif 18 < output_df['ego_velocity_x'][i] <= 19:
            if m_a_accln > 3.13:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False
        else:
            if m_a_accln > 3:
                if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
                    temp_df['KPI pass Flag'][i] = False

        kpi_pass_flag_list.append(str(temp_df['KPI pass Flag'][i]))

    output_df['ego_acc_x'] = ego_acc_x_list
    output_df['KPI_pass_Flag'] = kpi_pass_flag_list
    output_df['LCA_flag_on'] = LCA_flag_on

    output = output_df.to_dict('records')
    with open("l1_longitudinal_deceleration.csv", 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[key for key in output[0].keys()])
        writer.writeheader()
        writer.writerows(output)


def analyze_kpi_flag(ma_acc, ma_acc_thr, out_frame, temp_frame, index):
    if ma_acc > ma_acc_thr:
        if out_frame['ad_start'][index] == '1' or out_frame['ad_start'][index] == '1.0':
            temp_frame['KPI pass Flag'][index] = False


def check_longitudinal_deceleration_ccn():
    ground_truth_data = pd.read_parquet(file_path)

    # Extracting l1_longitudinal_deceleration_kpi KPI
    LCA_flag_on = True

    output_df = pd.DataFrame()
    output_df['timestamp'] = ground_truth_data["timestamp"]
    output_df['scenario_uuid'] = ground_truth_data["scenario_uuid"]
    output_df['date_id'] = ground_truth_data["date_id"]
    output_df['ad_start'] = ground_truth_data["ad_start"]
    output_df['current_timestamp'] = ground_truth_data["current_timestamp"]

    output_df['ego_velocity_x'] = np.sqrt(
        ground_truth_data["ego_velocity_x"] ** 2 + ground_truth_data["ego_velocity_y"] ** 2)
    output_df['ego_acc_x'] = np.sqrt(
        ground_truth_data["ego_acc_x"] ** 2 + ground_truth_data["ego_acc_y"] ** 2)

    temp_df = pd.DataFrame()
    temp_df['timestamp'] = ground_truth_data["timestamp"]
    temp_df['KPI pass Flag'] = True

    ego_acc_x_list = list()
    kpi_pass_flag_list = list()
    m_a_time_1004 = 2
    for i in range(len(output_df['current_timestamp'])):
        if len(ego_acc_x_list) > 0:
            sample_time = output_df['current_timestamp'][i] - output_df['current_timestamp'][i - 1]
        else:
            sample_time = 0

        if sample_time != 0:
            samples = int(m_a_time_1004 / sample_time)
        else:
            samples = 1

        if samples > i > 0:
            m_a_accln = output_df['ego_acc_x'][0:i].sum() / i
        elif i > samples:
            m_a_accln = output_df['ego_acc_x'][i - samples:i].sum() / samples
        else:
            m_a_accln = output_df['ego_acc_x'][0]
        ego_acc_x_list.append(m_a_accln)

        selector = {
            lambda velocity: velocity <= 5: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=5,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 5 < velocity <= 6: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.87,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 6 < velocity <= 7: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.73,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 7 < velocity <= 8: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.6,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 8 < velocity <= 9: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.47,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 9 < velocity <= 10: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.33,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 10 < velocity <= 11: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.2,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 11 < velocity <= 12: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=4.07,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 12 < velocity <= 13: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.93,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 13 < velocity <= 14: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.8,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 14 < velocity <= 15: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.67,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 15 < velocity <= 16: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.53,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 16 < velocity <= 17: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.4,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 17 < velocity <= 18: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.27,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            ),
            lambda velocity: 18 < velocity <= 19: analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3.13,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            )

        }

        selected = [selector[x] for x in selector if x(output_df['ego_velocity_x'][i])]
        if not selected:
            analyze_kpi_flag(
                ma_acc=m_a_accln,
                ma_acc_thr=3,
                out_frame=output_df,
                temp_frame=temp_df,
                index=i
            )

        # if output_df['ego_velocity_x'][i] <= 5:
        #     if m_a_accln > 5:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 5 < output_df['ego_velocity_x'][i] <= 6:
        #     if m_a_accln > 4.87:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 6 < output_df['ego_velocity_x'][i] <= 7:
        #     if m_a_accln > 4.73:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 7 < output_df['ego_velocity_x'][i] <= 8:
        #     if m_a_accln > 4.6:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 8 < output_df['ego_velocity_x'][i] <= 9:
        #     if m_a_accln > 4.47:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 9 < output_df['ego_velocity_x'][i] <= 10:
        #     if m_a_accln > 4.33:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 10 < output_df['ego_velocity_x'][i] <= 11:
        #     if m_a_accln > 4.2:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 11 < output_df['ego_velocity_x'][i] <= 12:
        #     if m_a_accln > 4.07:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 12 < output_df['ego_velocity_x'][i] <= 13:
        #     if m_a_accln > 3.93:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 13 < output_df['ego_velocity_x'][i] <= 14:
        #     if m_a_accln > 3.8:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 14 < output_df['ego_velocity_x'][i] <= 15:
        #     if m_a_accln > 3.67:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 15 < output_df['ego_velocity_x'][i] <= 16:
        #     if m_a_accln > 3.53:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 16 < output_df['ego_velocity_x'][i] <= 17:
        #     if m_a_accln > 3.4:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 17 < output_df['ego_velocity_x'][i] <= 18:
        #     if m_a_accln > 3.27:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # elif 18 < output_df['ego_velocity_x'][i] <= 19:
        #     if m_a_accln > 3.13:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False
        # else:
        #     if m_a_accln > 3:
        #         if output_df['ad_start'][i] == '1' or output_df['ad_start'][i] == '1.0':
        #             temp_df['KPI pass Flag'][i] = False

        kpi_pass_flag_list.append(str(temp_df['KPI pass Flag'][i]))

    output_df['ego_acc_x'] = ego_acc_x_list
    output_df['KPI_pass_Flag'] = kpi_pass_flag_list
    output_df['LCA_flag_on'] = LCA_flag_on

    output = output_df.to_dict('records')
    with open("l1_longitudinal_deceleration_ccn.csv", 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[key for key in output[0].keys()])
        writer.writeheader()
        writer.writerows(output)


if __name__ == '__main__':
    check_longitudinal_deceleration()
    check_longitudinal_deceleration_ccn()
