import json
from pprint import pprint


class Manager(object):
    def __init__(self):
        print("Constructor is initialized!")

    @staticmethod
    def create_something(info):
        print(info)

    def main(self):
        Manager.create_something("Im not a part of the class")


records = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0',
                  'EventSubscriptionArn': 'arn:aws:sns:us-east-1:911626952550:kpi-standard-topic:29610dd9-fffb-42d5-ab11-c54fa2be5dbf',
                  'Sns': {'Type': 'Notification', 'MessageId': '214d40f9-7196-5bc3-8e78-1bed6615e827',
                          'TopicArn': 'arn:aws:sns:us-east-1:911626952550:kpi-standard-topic',
                          'Subject': 'Amazon S3 Notification',
                          'Message': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2022-06-03T14:05:53.726Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AIDA5IQJTL5TIHPE33TC7"},"requestParameters":{"sourceIPAddress":"120.138.12.222"},"responseElements":{"x-amz-request-id":"5EAD7HRNSA8C13VX","x-amz-id-2":"rnDw9eJlqmuFDCN2yVrQxK3aQRRxxzKAAYAq6jeOIwJzD4SUd5d75LPVJcy+PAR68+u5eVn3N1fd5kZJQx8tN/V8LRa8twUt"},"s3":{"s3SchemaVersion":"1.0","configurationId":"kpi","bucket":{"name":"my-athena-scenario","ownerIdentity":{"principalId":"A3B8UDQNQSR6WA"},"arn":"arn:aws:s3:::my-athena-scenario"},"object":{"key":"data/bench1/1654265150457-681e15c5-43b2-4ae0-ab2b-4ea5977fb388-i-0151e095ae5e9626a/Reprocessed_Output/xosc_9f1d94bd-aabc-41a7-adf1-5f9502a833a1/ground_truth_kpi.parquet","size":5842833,"eTag":"957fa5f3ae62670302ba7448bdfdd4cd","sequencer":"00629A153F63FD75FB"}}}]}',
                          'Timestamp': '2022-06-03T14:05:55.495Z', 'SignatureVersion': '1',
                          'Signature': 'pOIgfVq+KLxWcYhacmgqTnQSTWdPjK5rTPQCIaNROw19zudl+gCzz7g4De+kxgVtYp7AS8O0OxaDWo1AhrXX7CNkcFkAq+h+oiWGvBbXxXNae5oNBh420gDc5wWp+lQ3H3VjhBUsCQtjHLEOveuI4el1QjBqBTGYKn4stNGRfzB9i3HJiDkWh/lc25UcKwjydjhYDZMtNyfuoV4Q3jCs93/fGp3/RSfGkesosV1AUnAbJTtIJkcQ+1RE7pBgiwMwnxxVF53Sro98GCE0TLnM6ETQE53K6cHybnEzqtBxXlcRoCMKEG+Y+xXCatjZJErS/ZFlOD8cbIb9tdjy97Xzdg==',
                          'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem',
                          'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:911626952550:kpi-standard-topic:29610dd9-fffb-42d5-ab11-c54fa2be5dbf',
                          'MessageAttributes': {}}}]}

if __name__ == "__main__":
    manage = Manager()
    manage.main()
    pprint(records['Records'][0]['Sns']['Message'])
    message = records['Records'][0]['Sns']['Message']
    if isinstance(message, str):
        message = json.loads(message)
    pprint(message['Records'][0]['s3']['bucket']['name'])
    pprint(message['Records'][0]['s3']['object']['key'])
    # pprint(json.loads('{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2022-06-03T14:05:53.726Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AIDA5IQJTL5TIHPE33TC7"},"requestParameters":{"sourceIPAddress":"120.138.12.222"},"responseElements":{"x-amz-request-id":"5EAD7HRNSA8C13VX","x-amz-id-2":"rnDw9eJlqmuFDCN2yVrQxK3aQRRxxzKAAYAq6jeOIwJzD4SUd5d75LPVJcy+PAR68+u5eVn3N1fd5kZJQx8tN/V8LRa8twUt"},"s3":{"s3SchemaVersion":"1.0","configurationId":"kpi","bucket":{"name":"my-athena-scenario","ownerIdentity":{"principalId":"A3B8UDQNQSR6WA"},"arn":"arn:aws:s3:::my-athena-scenario"},"object":{"key":"data/bench1/1654265150457-681e15c5-43b2-4ae0-ab2b-4ea5977fb388-i-0151e095ae5e9626a/Reprocessed_Output/xosc_9f1d94bd-aabc-41a7-adf1-5f9502a833a1/ground_truth_kpi.parquet","size":5842833,"eTag":"957fa5f3ae62670302ba7448bdfdd4cd","sequencer":"00629A153F63FD75FB"}}}]}'))
