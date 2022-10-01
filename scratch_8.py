import os
import json
import unittest


def read_json_file(file_path):
    with open(file_path) as file_obj:
        data = json.load(file_obj)
    return data


class TestReadJsonFile(unittest.TestCase):
    def setUp(self) -> None:
        print("Setup is called")
        self.root_dir = os.path.abspath(os.path.dirname(__name__))
        print(self.root_dir)
        self.file_name = 'info.json'
        self.file_data = [
            {
                "name": "Vikrant",
                "hobby": ["Coding", "Reading blogs"]
            }
        ]
        with open(os.path.join(self.root_dir, self.file_name), mode='w') as file_obj:
            json.dump(self.file_data, file_obj, indent=2)

    def tearDown(self) -> None:
        print("Tear Down is called")
        path = os.path.join(self.root_dir, self.file_name)
        if os.path.exists(path):
            os.remove(path)

    def test_read_json_file(self):
        print("test read_json_file")
        response = read_json_file(file_path=os.path.join(self.root_dir, self.file_name))
        # assert response[0]['name'] == self.file_data[0]['name']
        # assert response[0]['hobby'][0] == self.file_data[0]['hobby'][0]
        # assert response[0]['hobby'][1] == self.file_data[0]['hobby'][1]
        self.assertListEqual(response, self.file_data)
