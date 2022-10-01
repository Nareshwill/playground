import boto3

client = boto3.client('ec2')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
print(regions)