import pandas as pd
import os


def read_parquet_file(file_path=''):
    """
        Reads .parquet file and converts
        into a dataframe.
    """
    if os.path.exists(file_path):
        dataframe = pd.read_parquet(file_path)
        return dataframe
    return pd.DataFrame()


if __name__ == "__main__":
    print(len(read_parquet_file('ground_truth_kpi.parquet').to_dict('records')))
