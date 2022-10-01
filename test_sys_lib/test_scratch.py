import sys
import unittest
# from scratch import add
from unittest.mock import patch
from scratch import list_pop
# import pandas as pd


class TestScratch(unittest.TestCase):
    # def test_scratch(self):
    #     from scratch import main
    #     response = main()
    #     print(response)

    # def test_mock_scratch(self):
    #     with self.assertRaises(AttributeError):
    #         with patch.object(sys, 'argv', {}):
    #             from scratch import main
    #             response = main()
    #             print(response)

        with patch('builtins.list.pop', ''):
            response = list_pop()
            print("List Pop Response", response)

        # with patch.object(pd, "DataFrame", "Mock"):
        #     # mock_pd.return_value.loc.return_value = Mock(return_value=Mock())
        #     # mock_pd.return_value.loc.return_value.drop_duplicates.return_value = Mock()
        #     from scratch import df_inSOMEIP

# class TestAdd(unittest.TestCase):
#     root_path = None
#
#     @classmethod
#     def setUpClass(cls):
#         print("It will execute before all the test cases starts execution")
#         cls.root_path = 'test_scratch.py'
#
#     @classmethod
#     def tearDownClass(cls):
#         print("It will execute after all the test cases completes execution")
#         cls.root_path = None
#
#     def test_add(self):
#         print("Class Variable root_path", self.root_path)
#         response = add(a=2, b=4)
#         self.assertEqual(response, 6)

