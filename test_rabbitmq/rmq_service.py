import pika

RABBIT_MQ_HOST = 'localhost'


class RMQConnection(object):
    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_MQ_HOST)
        )
        self.channel = self.connection.channel()
        return self.channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class RabbitMqService:
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def push(self, message_body='empty'):
        with RMQConnection() as channel:
            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message_body
            )

    def pop(self):
        with RMQConnection() as channel:
            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)
            method_frame, header_frame, body = channel.basic_get(queue=self.queue_name)
            if not method_frame:
                message = 'No message received'
            elif method_frame and method_frame.NAME == 'Basic.GetEmpty':
                message = 'No message received'
            else:
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                message = body.decode()
        return message

    def delete_message(self):
        pass

    def __len__(self):
        with RMQConnection() as channel:
            queue = channel.queue_declare(queue=self.queue_name, durable=True)
            message_count = queue.method.message_count
        return message_count
