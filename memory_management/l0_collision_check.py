import os
import time
import math
import linecache
import tracemalloc
import numpy as np
import pandas as pd
from pymongo import MongoClient


def evaluate(data):
    if data:
        if False not in [row.get('kpi_pass_flag') for row in data]:
            return "pass"
        else:
            return "fail"
    return "Not available"


file_name = 'ground_truth_kpi.parquet'

tracemalloc.start()
start_time = time.time()
ground_truth_data = pd.read_parquet(file_name)

print("Casted to a dataframe")
# Extracting l0_collision_check_kpi KPI
longitudnal_tolerance = 1
lateral_tolerance = 0.5
target_previous_distance = dict()

output_df = pd.DataFrame()
output_df['timestamp'] = ground_truth_data["timestamp"]
output_df['scenario_uuid'] = ground_truth_data["scenario_uuid"]
output_df['date_id'] = ground_truth_data["date_id"]
output_df['ad_start'] = ground_truth_data["ad_start"]

output_df['current_timestamp'] = ground_truth_data["current_timestamp"]
output_df['ego_location_x'] = ground_truth_data["ego_location_x"]
output_df['ego_location_y'] = ground_truth_data["ego_location_y"]
output_df['ego_length_half'] = ground_truth_data["ego_length_half"]
output_df['ego_width_half'] = ground_truth_data["ego_width_half"]
output_df['ego_yaw'] = ground_truth_data["ego_yaw"]

output_df["traffic_vehicle_location_x"] = ground_truth_data["traffic_vehicle_location_x"].apply(eval)
output_df["traffic_vehicle_location_y"] = ground_truth_data["traffic_vehicle_location_y"].apply(eval)
output_df["traffic_vehicle_length_half"] = ground_truth_data["traffic_vehicle_length_half"].apply(eval)
output_df["traffic_vehicle_width_half"] = ground_truth_data["traffic_vehicle_width_half"].apply(eval)

ego_net_velocity = np.sqrt((ground_truth_data['ego_velocity_x'] ** 2) + (ground_truth_data['ego_velocity_y'] ** 2))

waypoint_data = (ground_truth_data['waypoint'])
waypoint_x_val = waypoint_data.str.split("Location\\(",
                                         expand=True)[1].str.split(",", expand=True)[
    0].str.strip().str.split("x=", expand=True)[1]
waypoint_x = waypoint_x_val.apply(float)
waypoint_y_val = waypoint_data.str.split("Location\\(",
                                         expand=True)[1].str.split(",", expand=True)[
    1].str.strip().str.split("y=", expand=True)[1]
waypoint_y = waypoint_y_val.apply(float)

waypoint_local_x = waypoint_x - output_df["ego_location_x"]
waypoint_local_y = waypoint_y - output_df['ego_location_y']

waypoint_local_y_val = np.sin(
    output_df['ego_yaw'] / 57.3) * waypoint_local_x + np.cos(
    output_df['ego_yaw'] / 57.3) * waypoint_local_y

output_df["kpi_pass_flag"] = True
output_df["collision_target"] = 'Null'

longitudinal_gap_with_tv_list = list()
lateral_gap_with_tv_list = list()

for i in range(len(ground_truth_data["ego_lane_id"])):
    ego_lane_id = float(ground_truth_data["ego_lane_id"][i])

    target_lane_id = eval(ground_truth_data['traffic_vehicle_lane_id'][i])

    if len(longitudinal_gap_with_tv_list) == 0:
        target_previous_distance = dict()
        ego_previous_distance = 0
        previous_time = output_df['current_timestamp'][i]

    sample_time = (ground_truth_data['current_timestamp'][i]) - previous_time
    previous_time = (ground_truth_data['current_timestamp'][i])
    ego_current_distance = ego_previous_distance + \
                           (ego_net_velocity[i] * sample_time)
    ego_previous_distance = ego_current_distance

    tv_role = list(output_df["traffic_vehicle_location_x"][i].keys())

    longitudinal_gap_with_tv_list.append(dict())
    lateral_gap_with_tv_list.append(dict())
    for target_iterator in range(len(tv_role)):
        tv_net_velocity = math.sqrt(
            float(
                eval(
                    ground_truth_data['traffic_vehicle_velocity_x'][i])[
                    tv_role[target_iterator]]) ** 2 +
            float(
                eval(
                    ground_truth_data['traffic_vehicle_velocity_y'][i])[
                    tv_role[target_iterator]]) ** 2)

        if tv_role[target_iterator] not in target_previous_distance.keys():
            if 'initial_distance' in output_df.keys():
                target_previous_distance[tv_role[target_iterator]] = eval(
                    output_df['initial_distance'])[tv_role[target_iterator]] + ego_current_distance
            else:
                target_previous_distance[
                    tv_role[target_iterator]] = math.sqrt(
                    float(
                        eval(
                            ground_truth_data["traffic_vehicle_location_x"][i])[
                            tv_role[target_iterator]] - output_df['ego_location_x'][i]) ** 2 + float(
                        eval(
                            ground_truth_data["traffic_vehicle_location_y"][i])[
                            tv_role[target_iterator]] - output_df['ego_location_y'][i]) ** 2) + ego_current_distance

        tv_current_distance = float(
            target_previous_distance[tv_role[target_iterator]]) + (tv_net_velocity * sample_time)

        target_previous_distance[tv_role[target_iterator]
        ] = tv_current_distance

        longitudinal_gap_with_tv_list[i][tv_role[target_iterator]] = abs(
            tv_current_distance - ego_current_distance) - output_df['ego_length_half'][i] - \
                                                                     output_df["traffic_vehicle_length_half"][i][
                                                                         tv_role[target_iterator]]
        tv_waypoint_data = eval(ground_truth_data['traffic_vehicle_waypoint'][i])[
            tv_role[target_iterator]]
        tv_waypoint_x_val = tv_waypoint_data.split(
            "Location(")[-1].split(',')[0].strip().split("x=")[-1]
        tv_waypoint_x = float(tv_waypoint_x_val)
        tv_waypoint_y_val = tv_waypoint_data.split(
            "Location(")[-1].split(',')[1].strip().split("y=")[-1]
        tv_waypoint_y = float(tv_waypoint_y_val)
        tv_yaw = float(tv_waypoint_data.split(
            "Rotation(")[-1].split(',')[1].strip().split("yaw=")[-1])
        tv_waypoint_local_x = tv_waypoint_x - \
                              output_df["traffic_vehicle_location_x"][i][tv_role[target_iterator]]
        tv_waypoint_local_y = tv_waypoint_y - \
                              output_df["traffic_vehicle_location_y"][i][tv_role[target_iterator]]
        # tv_waypoint_local_x_val = math.cos(
        #     tv_yaw / 57.3) * tv_waypoint_local_x - math.sin(tv_yaw / 57.3) * tv_waypoint_local_y
        tv_waypoint_local_y_val = math.sin(
            tv_yaw / 57.3) * tv_waypoint_local_x + math.cos(tv_yaw / 57.3) * tv_waypoint_local_y

        tv_laneOffset = tv_waypoint_local_y_val

        if target_lane_id[tv_role[target_iterator]] == ego_lane_id:
            lateral_gap = 0
        else:
            lateral_gap = (abs(target_lane_id[tv_role[target_iterator]] - ego_lane_id) * 3.5) - tv_laneOffset + \
                          waypoint_local_y_val[i] - \
                          output_df["ego_width_half"][i] - \
                          output_df["traffic_vehicle_width_half"][i][tv_role[target_iterator]]

        if lateral_gap > 5.5:
            lateral_gap = 5.5

        lateral_gap_with_tv_list[i][tv_role[target_iterator]
        ] = lateral_gap
        if (abs(longitudinal_gap_with_tv_list[i][tv_role[target_iterator]])) <= longitudnal_tolerance and abs(
                lateral_gap_with_tv_list[i][tv_role[target_iterator]]) <= lateral_tolerance:
            output_df['collision_target'][i] = tv_role[target_iterator]
            if output_df["ad_start"][i] == '1' or output_df["ad_start"][i] == '1.0':
                output_df['kpi_pass_flag'][i] = False

output_df["longitudinal_gap_with_tv"] = longitudinal_gap_with_tv_list
output_df["lateral_gap_with_tv"] = lateral_gap_with_tv_list

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


def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


display_top(tracemalloc.take_snapshot())
print("Utilized Memory: ", tracemalloc.get_tracemalloc_memory())
tracemalloc.stop()
