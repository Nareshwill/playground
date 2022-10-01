# Checking False Indicator Check
import csv
import pandas as pd
import numpy as np

file_path = '/home/kpit/execution/ground_truth_kpi.parquet'


def false_indicator_check():
    ground_truth_data = pd.read_parquet(file_path)

    print("Casted to a dataframe")
    # Extracting l0_collision_check KPI
    output_df = pd.DataFrame()
    output_df['timestamp'] = ground_truth_data["timestamp"]
    output_df['scenario_uuid'] = ground_truth_data["scenario_uuid"]
    output_df['date_id'] = ground_truth_data["date_id"]
    output_df['ad_start'] = ground_truth_data["ad_start"]

    output_df['current_timestamp'] = ground_truth_data['current_timestamp']
    output_df['ego_width_half'] = ground_truth_data['ego_width_half']
    output_df['waypoint'] = ground_truth_data['waypoint']
    output_df['right_lane_waypoint'] = ground_truth_data['right_lane_waypoint']
    output_df['left_lane_waypoint'] = ground_truth_data['left_lane_waypoint']
    output_df['ego_yaw'] = ground_truth_data['ego_yaw']
    output_df['ego_location_y'] = ground_truth_data['ego_location_y']
    output_df['ego_location_x'] = ground_truth_data['ego_location_x']
    output_df['right_lane_type'] = ground_truth_data['right_lane_type']
    output_df['left_lane_type'] = ground_truth_data['left_lane_type']
    output_df['ev_right_blinker'] = False
    output_df['ev_left_blinker'] = False

    waypoint_data = (ground_truth_data['waypoint'])
    waypoint_x_val = waypoint_data.str.split("Location\\(",
                                             expand=True)[1].str.split(",", expand=True)[
        0].str.strip().str.split("x=", expand=True)[1]
    waypoint_x = waypoint_x_val.apply(float)
    waypoint_y_val = waypoint_data.str.split("Location\\(",
                                             expand=True)[1].str.split(",", expand=True)[
        1].str.strip().str.split("y=", expand=True)[1]
    waypoint_y = waypoint_y_val.apply(float)

    # temp_df = pd.DataFrame()
    # temp_df["ego_location_x"] = ground_truth_data["ego_location_x"].apply(float)

    waypoint_local_x = waypoint_x - output_df["ego_location_x"]
    waypoint_local_y = waypoint_y - output_df['ego_location_y']

    waypoint_local_y_val = np.sin(
        output_df['ego_yaw'] / 57.3) * waypoint_local_x + np.cos(
        output_df['ego_yaw'] / 57.3) * waypoint_local_y

    output_df['lane_offset'] = waypoint_local_y_val

    output_df['lane_availability'] = 1
    output_df['kpi_pass_flag'] = True

    for i in range(len(ground_truth_data["current_timestamp"])):
        # to avoid SettingWithCopyWarning.
        pd.options.mode.chained_assignment = None
        if output_df['lane_offset'][i] > (
                1.75 - (output_df['ego_width_half'][i])):
            if output_df['right_lane_type'][i] == '' or ((output_df['right_lane_type'][i] != '2') and (
                    output_df['right_lane_type'][i] != 'Driving')):
                output_df['lane_availability'][i] = 0
                if output_df['ev_right_blinker'][i]:
                    if output_df["ad_start"][i] == '1' or output_df["ad_start"][i] == '1.0':
                        output_df['kpi_pass_flag'][i] = False
        elif output_df['lane_offset'][i] < -(1.75 - (output_df['ego_width_half'][i])):
            if output_df['left_lane_type'][i] == '' or ((output_df['left_lane_type'][i] != '2') and (
                    output_df['left_lane_type'][i] != 'Driving')):
                output_df['lane_availability'][i] = 0
                if output_df['ev_left_blinker'][i]:
                    if output_df["ad_start"][i] == '1' or output_df["ad_start"][i] == '1.0':
                        output_df['kpi_pass_flag'][i] = False

    output = output_df.to_dict('records')
    with open("l0_false_indicator_check.csv", 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[key for key in output[0].keys()])
        writer.writeheader()
        writer.writerows(output)


def analyze_kpi_flag(right, left, out_frame, index):
    if (right or left) and (out_frame['ev_right_blinker'][index] or out_frame['ev_left_blinker'][index]) and (
            out_frame["ad_start"][index] == '1' or out_frame["ad_start"][index] == '1.0'):
        out_frame['kpi_pass_flag'][index] = False


def check_false_indicator_ccn():
    ground_truth_data = pd.read_parquet(file_path)

    print("Casted to a dataframe")
    # Extracting l0_collision_check KPI
    output_df = pd.DataFrame()
    output_df['timestamp'] = ground_truth_data["timestamp"]
    output_df['scenario_uuid'] = ground_truth_data["scenario_uuid"]
    output_df['date_id'] = ground_truth_data["date_id"]
    output_df['ad_start'] = ground_truth_data["ad_start"]

    output_df['current_timestamp'] = ground_truth_data['current_timestamp']
    output_df['ego_width_half'] = ground_truth_data['ego_width_half']
    output_df['waypoint'] = ground_truth_data['waypoint']
    output_df['right_lane_waypoint'] = ground_truth_data['right_lane_waypoint']
    output_df['left_lane_waypoint'] = ground_truth_data['left_lane_waypoint']
    output_df['ego_yaw'] = ground_truth_data['ego_yaw']
    output_df['ego_location_y'] = ground_truth_data['ego_location_y']
    output_df['ego_location_x'] = ground_truth_data['ego_location_x']
    output_df['right_lane_type'] = ground_truth_data['right_lane_type']
    output_df['left_lane_type'] = ground_truth_data['left_lane_type']
    output_df['ev_right_blinker'] = False
    output_df['ev_left_blinker'] = False

    waypoint_data = (ground_truth_data['waypoint'])
    waypoint_x_val = waypoint_data.str.split("Location\\(",
                                             expand=True)[1].str.split(",", expand=True)[
        0].str.strip().str.split("x=", expand=True)[1]
    waypoint_x = waypoint_x_val.apply(float)
    waypoint_y_val = waypoint_data.str.split("Location\\(",
                                             expand=True)[1].str.split(",", expand=True)[
        1].str.strip().str.split("y=", expand=True)[1]
    waypoint_y = waypoint_y_val.apply(float)

    # temp_df = pd.DataFrame()
    # temp_df["ego_location_x"] = ground_truth_data["ego_location_x"].apply(float)

    waypoint_local_x = waypoint_x - output_df["ego_location_x"]
    waypoint_local_y = waypoint_y - output_df['ego_location_y']

    waypoint_local_y_val = np.sin(
        output_df['ego_yaw'] / 57.3) * waypoint_local_x + np.cos(
        output_df['ego_yaw'] / 57.3) * waypoint_local_y

    output_df['lane_offset'] = waypoint_local_y_val

    output_df['lane_availability'] = 1
    output_df['kpi_pass_flag'] = True

    for i in range(len(ground_truth_data["current_timestamp"])):
        # to avoid SettingWithCopyWarning.
        pd.options.mode.chained_assignment = None
        right_condition = False
        left_condition = False
        if output_df['lane_offset'][i] > (
                1.75 - (output_df['ego_width_half'][i])):
            if output_df['right_lane_type'][i] == '' or ((output_df['right_lane_type'][i] != '2') and (
                    output_df['right_lane_type'][i] != 'Driving')):
                output_df['lane_availability'][i] = 0
                right_condition = True
                # if output_df['ev_right_blinker'][i]:
                #     if output_df["ad_start"][i] == '1' or output_df["ad_start"][i] == '1.0':
                #         output_df['kpi_pass_flag'][i] = False
        elif output_df['lane_offset'][i] < -(1.75 - (output_df['ego_width_half'][i])):
            if output_df['left_lane_type'][i] == '' or ((output_df['left_lane_type'][i] != '2') and (
                    output_df['left_lane_type'][i] != 'Driving')):
                output_df['lane_availability'][i] = 0
                left_condition = True
                # if output_df['ev_left_blinker'][i]:
                #     if output_df["ad_start"][i] == '1' or output_df["ad_start"][i] == '1.0':
                #         output_df['kpi_pass_flag'][i] = False

        analyze_kpi_flag(
            right=right_condition,
            left=left_condition,
            out_frame=output_df,
            index=i
        )

    output = output_df.to_dict('records')
    with open("l0_false_indicator_check_ccn.csv", 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[key for key in output[0].keys()])
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    false_indicator_check()
    check_false_indicator_ccn()
