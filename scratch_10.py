import unittest
from unittest import mock
from unittest.mock import Mock

import pytest
from scratch_11 import make_multiple_requests, going_to_be_mocked


class MockMultipleRequest(unittest.TestCase):
    @mock.patch('requests.get')
    def test_make_multiple_requests(self, fake_get_request):
        fake_responses = [Mock(), Mock()]
        fake_responses[0].json.return_value = [
            {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False},
            {'userId': 1, 'id': 2, 'title': 'quis ut nam facilis et officia qui', 'completed': False},
            {'userId': 1, 'id': 3, 'title': 'fugiat veniam minus', 'completed': False}
        ]
        fake_responses[0].status_code = 200

        fake_responses[1].json.return_value = [
            {'userId': 10, 'id': 197, 'title': 'dignissimos quo nobis earum saepe', 'completed': True}
        ]
        fake_responses[1].status_code = 200
        fake_get_request.side_effect = fake_responses

        response = make_multiple_requests()
        print(response)


@pytest.mark.going_to_be_mocked
class TestGoingToBeMocked(unittest.TestCase):
    @mock.patch('scratch_11.throw_values')
    def test_going_to_be_mocked_bad_response(self, fake_throw_values):
        with self.assertRaises(Exception):
            fake_throw_values.return_value = ''
            response = going_to_be_mocked()
            print(response)
            raise TypeError

    def test_going_to_be_mocked_proper_response(self):
        response = going_to_be_mocked()
        self.assertEqual(response, 'Type foo')


if __name__ == '__main__':
    unittest.main()
