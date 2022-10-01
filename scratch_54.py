import sys
import configparser

print(sys.argv)

config = configparser.ConfigParser()
config_path = '/home/kpit/code/other-projects/r.0033914.001_intcom_handler-develop/input/Config.ini'
config.read(config_path)

sections = config.sections()

for section in sections:
    print(section)
    print(config[section].get('File'))
    
# python3 ../py_code/E2A_arxmlGenerator.py "../interim/E4A.xlsx" "../output/PortsLinking.xlsx" "../input/COM_config.ini"
