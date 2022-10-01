import unittest

# import mock
import pika
import rmq_service
from unittest.mock import Mock, patch, MagicMock
from rmq_service import RMQConnection, RabbitMqService
# from pytest_rabbitmq import factories

# rabbitmq_my_proc = factories.rabbitmq_proc(
#     port=None, logsdir='/tmp')
# rabbitmq_my = factories.rabbitmq('rabbitmq_my_proc')


# class Channel(object):
#     def __init__(self):
#         self.queue = ''
#         self.message = ''
#         self.exchange = ''
#
#     def declare(self, queue=None, durable=False):
#         pass
#
#     def basic_publish(self, exchange='', routing_key='', body=''):
#         self.message = body
#         self.queue = routing_key
#         self.exchange = exchange
#         return True
#
#
# def load_channel():
#     return Channel()


# class TestRabbitMqService(unittest.TestCase):
#     def test_push(self):
#         # with mock.patch.object(RMQConnection, '__enter__', new=load_channel):
#         #     rmq = RabbitMqService(queue_name='test-queue')
#         #     rmq.push(message_body=str({"name": "Kobe Bryant"}))
#
#         mock_service = RabbitMqService
#         mock_service.push = Mock(return_value=None)
#
#         rmq = RabbitMqService(queue_name='test-queue')
#         response = rmq.push(message_body=str({"name": "Kobe Bryant"}))
#         self.assertIsNone(response)
#
#     def test_pop(self):
#         message = str({'name': 'Kobe Bryant'})
#
#         mock_object = RabbitMqService
#         mock_object.pop = Mock(return_value=message)
#
#         rmq = RabbitMqService(queue_name='test-queue')
#         response = rmq.pop()
#         self.assertEqual(message, response)
#
#     def test_length(self):
#         mock_object = RabbitMqService
#         mock_object.__len__ = Mock(return_value=0)
#
#         rmq = RabbitMqService(queue_name='test-queue')
#         self.assertEqual(len(rmq), 0)


# class TestRMQConnection(unittest.TestCase):
#
#     @patch('rmq_service.RMQConnection')
#     def test__enter__(self, mock_rmq_connection):
#         RMQConnection()
#         assert mock_rmq_connection is rmq_service.RMQConnection
#
#
# class TestRabbitMq(unittest.TestCase):
#     def test_push(self):
#         rmq = RabbitMqService(queue_name='test-queue')
#         response = rmq.push(message_body='Hi')
#         self.assertIsNone(response)
#
#     def test_pop(self):
#         message_sent = str({'name': 'Kobe Bryant'})
#         rmq = RabbitMqService(queue_name='test-queue')
#         rmq.push(message_body=message_sent)
#         response = rmq.pop()
#         self.assertEqual(message_sent, response)
#
#
# class TestRMq(unittest.TestCase):
#     # @mock.patch.object(pika.BlockingConnection.channel)
#     @mock.patch('pika.BlockingConnection')
#     def test_mq(self, mocked_connection):
#         mocked_connection.return_value.channel.return_value.basic_publish.return_value = False
#         message_sent = str({'name': 'Kobe Bryant'})
#         rmq = RabbitMqService(queue_name='test-queue')
#         rmq.push(message_body=message_sent)
#         response = rmq.pop()
#         self.assertEqual(message_sent, response)


class TestRabbitMqService(unittest.TestCase):

    def test_push(self):

        with patch('rmq_service.pika') as mock_pika:
            mock_pika.BlockingConnection.return_value = Mock(return_value=Mock())
            mock_pika.ConnectionParameters.return_value = Mock(return_value='ampq://localhost:5672/')
            # mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.return_value = True
            # mock_pika.BlockingConnection.return_value.channel.return_value.basic_publish.return_value = True

            rmq = RabbitMqService(queue_name='test-queue')
            rmq.push(message_body='Hi There!')
            mock_pika.BlockingConnection.assert_called_once()
            mock_pika.ConnectionParameters.assert_called_once()

    def test_pop(self):

        # Checking the if loop from pop() method
        with patch('rmq_service.pika') as mock_pika:
            mock_pika.BlockingConnection.return_value = Mock(return_value=Mock())
            mock_pika.ConnectionParameters.return_value = Mock(return_value='ampq://localhost:5672/')

            mock_pika.BlockingConnection.return_value.channel.return_value = Mock(return_value=Mock())
            mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.return_value = None
            mock_pika.BlockingConnection.return_value.channel.return_value.basic_get.return_value = False, None, ''

            rmq = RabbitMqService(queue_name='test-queue')
            response = rmq.pop()
            self.assertEqual(response, 'No message received')

        # Checking the elif basic_get.Name string property
        with patch('rmq_service.pika') as mock_pika:
            mock_pika.BlockingConnection.return_value = Mock(return_value=Mock())
            mock_pika.ConnectionParameters.return_value = Mock(return_value='ampq://localhost:5672/')

            mock_pika.BlockingConnection.return_value.channel.return_value = Mock(return_value=Mock())
            mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.return_value = None
            mock_basic_get = Mock()
            mock_basic_get.NAME = 'Basic.GetEmpty'
            mock_pika.BlockingConnection.return_value.channel.return_value.basic_get.return_value = mock_basic_get, None, ''

            rmq = RabbitMqService(queue_name='test-queue')
            response = rmq.pop()
            self.assertEqual(response, 'No message received')

        # Checking the pushed message
        message_sent = b'Hi There!'
        with patch('rmq_service.pika') as mock_pika:
            mock_pika.BlockingConnection.return_value = Mock(return_value=Mock())
            mock_pika.ConnectionParameters.return_value = Mock(return_value='ampq://localhost:5672/')

            mock_pika.BlockingConnection.return_value.channel.return_value = Mock(return_value=Mock())
            mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.return_value = None
            mock_basic_get = Mock()
            mock_pika.BlockingConnection.return_value.channel.return_value.basic_get.return_value = mock_basic_get, None, message_sent

            rmq = RabbitMqService(queue_name='test-queue')
            response = rmq.pop()
            self.assertEqual(message_sent.decode(), response)

    def test__len__(self):
        with patch('rmq_service.pika') as mock_pika:
            mock_pika.BlockingConnection.return_value = Mock(return_value=Mock())
            mock_pika.ConnectionParameters.return_value = Mock(return_value='ampq://localhost:5672/')

            mock_pika.BlockingConnection.return_value.channel.return_value = Mock(return_value=Mock())
            mock_message_object = MagicMock(return_value=1)
            mock_message_object.__len__.return_value = list()
            mock_message_object.message_count.return_value = list()
            mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.return_value = \
                mock_message_object

            rmq = RabbitMqService(queue_name='test-queue')
            self.assertEqual(len(rmq), 1)
