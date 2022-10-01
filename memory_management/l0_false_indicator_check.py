import time
import tracemalloc
import pandas as pd
import numpy as np
from pymongo import MongoClient


def evaluate(data):
    if data:
        if False not in [row.get('kpi_pass_flag') for row in data]:
            return "pass"
        else:
            return "fail"
    return "Not available"


tracemalloc.start()
start_time = time.time()
# Casting to a dataframe
file_name = 'ground_truth_kpi.parquet'
ground_truth_data = pd.read_parquet(file_name)

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

print("Conversion completed")
result = evaluate(data=output_df.to_dict('records'))
print("Evaluation completed")
print("Time taker: ", time.time() - start_time)
print("result", result)

client = MongoClient("mongodb://demouser1:password@localhost:27017/?authSource=close_loop_validation")
database = client['close_loop_validation']
collection = database['sample_status_record']

collection.insert_one({
    'result': result
})

print("Utilized Memory: ", tracemalloc.get_tracemalloc_memory())
tracemalloc.stop()
