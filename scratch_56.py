import unittest
from pprint import pprint
import sqlite3
import pandas as pd

connection = sqlite3.connect(
    '/home/kpit/code/other-projects/r.0033914.001_intcom_handler-develop/interim/arxml_cache.db')
cursor = connection.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print(tables)
for table_name in tables:
    table_name = table_name[0]  # tables is a list of single item tuples
    table = pd.read_sql_query("SELECT * from {} LIMIT 0".format(table_name), connection)
    print(table_name)
    for col in table.columns:
        print('\t' + col)
    print()

cursor.execute("SELECT * FROM Parsed_Data LIMIT 10;")
print(cursor.fetchall())

cursor.execute('''SELECT rowid,* FROM Parsed_Data
                WHERE tag_name=? AND value_string=? AND file_name=?''', ('short-name', 'AUTOSAR_Dcm', 'AdLfe.arxml'))
pprint(cursor.fetchall())


class TestDbCache(unittest.TestCase):
    def test__get_data_by_tag_value(self):
        from db_cache import DbCache
        db_obj = DbCache(cache_path="<db_path>", arxml_folder="<arxml_folder>")
        response = db_obj.__get_data_by_tag_value(
            name_of_tag='short-name', string_value='AUTOSAR_Dcm', name_of_file='AdLfe.arxml'
        )
        expected_payload = [(2, 'short-name', 'AUTOSAR_Dcm', -1.0, 0, 'AUTOSAR_Dcm', 'AdLfe.arxml'),
                            (165, 'short-name', 'AUTOSAR_Dcm', -1.0, 0, 'AUTOSAR_Dcm', 'AdLfe.arxml')]
        self.assertListEqual(response, expected_payload)
        
    def test_func(self):
        pass
