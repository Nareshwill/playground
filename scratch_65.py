import boto3
import uuid


class SQSService(object):

    def __init__(self, *args, **kwargs):
        if 'queue_name' not in kwargs:
            raise Exception("Expecting a 'queue_name' attribute to create/fetch queue name")
        if 'region_name' not in kwargs:
            raise Exception("Expecting a 'region_name' attribute to create/fetch queue name from specific region")

        self.queue_name = kwargs.get('queue_name')
        self.region_name = kwargs.get('region_name')
        self.sqs_client = boto3.client('sqs', region_name=self.region_name)
        try:
            self.queue_url = self.sqs_client.get_queue_url(QueueName=self.queue_name)
        except Exception as error:
            print(error)
            self.queue = self.sqs_client.create_queue(QueueName=self.queue_name,
                                                      Attributes={'ReceiveMessageWaitTimeSeconds': '0'})
            self.queue_url = self.sqs_client.get_queue_url(QueueName=self.queue_name)

    def publish_message(self, message_body):
        response = self.sqs_client.send_message(
            QueueUrl=self.queue_url['QueueUrl'], MessageBody=str(message_body))
        return response


if __name__ == '__main__':
    queue = 'kpi-evaluation-using-sqs-testing'
    message = {
        'scheduler_uuid': '6af24199-f0ec-4d2c-9f99-54b76e705ca5',
        'test_run_id': '1659518751190-084bd4e69d6f792b6-101e9dc2-0086-4eea-88c6-c3855e756441|i-084bd4e69d6f792b6',
        'scenario_group_id': 15,
        'scenario_uuid': '28c587a9-bd2e-4e95-88b7-d4fd2f20659e',
        'scenario_status': 'completed_with_success',
        'cad_topology_job_uuid': '1fffc901-b6d4-4c5e-a4b0-9cae8a06b41a',
        'job_id': 'd880ef85-664d-4d36-b8d0-3270e4037248',
        'bench_id': 11,
        'bench_name': 'Carla_Bench_1',
        'instance_id': 'i-084bd4e69d6f792b6',
        'docker_id': '101e9dc2-0086-4eea-88c6-c3855e756441|i-084bd4e69d6f792b6',
        'bucket_name': 'cclp-migration-data-test-02',
        'region_name': 'us-east-1',
    }
    queue_object = SQSService(queue_name=queue, region_name='us-east-1')
    response = queue_object.publish_message(message_body=str(message))
    print(response)
