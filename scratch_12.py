import csv
import os
from pprint import pprint
import plotly.graph_objects as go

VELOCITY_X = 'traffic_vehicle_velocity_x'
VELOCITY_Y = 'traffic_vehicle_velocity_y'


def transform_dtypes(csv_data):
    for row in csv_data:
        if row.get(VELOCITY_X, None):
            row[VELOCITY_X] = eval(row.get(VELOCITY_X))
        if row.get(VELOCITY_Y, None):
            row[VELOCITY_Y] = eval(row.get(VELOCITY_Y))
    return csv_data


def generate_graph(csv_path='', graph_name='original'):
    if os.path.exists(csv_path):
        csv_data = list(csv.DictReader(open(csv_path)))
        csv_data = transform_dtypes(csv_data=csv_data)
        print('No of Rows : ', len(csv_data))
        seconds = [int(info.get('timestamp')) - int(csv_data[0]['timestamp']) for info in csv_data]
        velocity_x_info = dict()
        for row in csv_data:
            if row.get(VELOCITY_X):
                for key in row.get(VELOCITY_X):
                    if key not in velocity_x_info:
                        velocity_x_info[key] = list()
                    velocity_x_info[key].append(row.get(VELOCITY_X)[key])

        line_chart_fig = go.Figure()
        for tv_info in velocity_x_info:
            line_chart_fig.add_trace(go.Scatter(
                x=seconds,
                y=velocity_x_info[tv_info],
                name=tv_info
            ))
            line_chart_fig.update_layout(
                title='Velocity X {}'.format(graph_name),
                xaxis_title='Seconds',
                yaxis_title=tv_info)
        directory = os.path.dirname(csv_path)
        line_chart_fig.write_image(os.path.join(directory, '{}.png'.format(graph_name)))


if __name__ == '__main__':
    generate_graph(csv_path="/home/kpit/Downloads/level0_level1_kpi-original.csv")
    # generate_graph(csv_path="/home/kpit/Downloads/level0_level1_kpi_generated.csv", graph_name='Generated')
