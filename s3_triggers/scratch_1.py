import boto3
from pymongo import MongoClient


client = boto3.client('s3')
bucket_name = "my-athena-scenario"

if __name__ == "__main__":
    mongo_client = MongoClient("mongodb://nareshc3:password@localhost:27017/?authSource=s3_triggers")
    database = mongo_client['s3_triggers']
    collection = database['upload_history']
    results = collection.find()
    for doc in results:
        response = client.delete_object(
            Bucket=bucket_name,
            Key=doc.get('path')
        )
        print(response)
        collection.delete_one({'path': doc.get('path')})
        print(collection.count_documents({}))
