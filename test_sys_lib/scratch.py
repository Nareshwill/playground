import sys

# import configparser


# import pandas as pd

print(sys.argv)


# print(sys.argv[1])

def main():
    first_element = sys.argv[0]
    if len(sys.argv) == 1:
        raise AttributeError("I need an command line arg to function this script")
    else:
        print(sys.argv)
    return first_element


def list_pop():
    data = [1, 2, 3]
    print(data.pop())


# rows = [
#     {"Source": "INVALID", "ServiceInterface": "EgoMotion_Acceleration", "EventName": "AccelerationLateralCog",
#      "EventDatatype": "AccelerationLateralCogType"},
#     {"Source": 0, "ServiceInterface": "EgoMotion_Acceleration", "EventName": "AccelerationLateralCog",
#      "EventDatatype": "AccelerationLateralCogType"}]
# print(pd)
# df_SOMEIP_all = pd.DataFrame(rows)
# df_inSOMEIP = df_SOMEIP_all.loc[:, ['Source', 'ServiceInterface', 'EventName', 'EventDatatype']].drop_duplicates(
#     keep='first', subset=['ServiceInterface', 'EventName', 'EventDatatype'], ignore_index=True)
# print(df_inSOMEIP)


def add(a, b):
    return a + b


def sub(a, b):
    return a - b

# open('Config.ini')
# 
# config = configparser.ConfigParser()  # creating of ConfigParser()
# config.read('Config.ini')
# 
# print(config.sections())
# for section in config.sections():
#     print(section)
# 
# tutorial_section = config['tutorial']
# print(tutorial_section.get('day1'))
# print(dict(tutorial_section))
