import requests
from pprint import pprint


def make_multiple_requests():
    endpoint = 'http://jsonplaceholder.typicode.com/todos'
    response_one = requests.get(
        endpoint
    )
    print(response_one)
    print(response_one.status_code)
    data_one = response_one.json()
    pprint(data_one)
    if len(data_one) <= 1:
        raise Exception("Expected more than one todo(s)")
    response_two = requests.get(
        '{}?id=199'.format(endpoint)
    )
    data_two = response_two.json()
    if len(data_two) > 1:
        raise Exception("Expected only one todo, but instead got more")
    print(data_two)
    return True


def throw_values():
    class Foo:
        def __init__(self):
            self.fn = 'Type foo'
    
    return Foo()


def going_to_be_mocked(info=''):
    try:
        mock_obj = throw_values()
        return mock_obj.fn
    except Exception as error:
        print(error)
        return 'error occurred'


if __name__ == "__main__":
    make_multiple_requests()
