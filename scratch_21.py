
from pymongo import MongoClient

client = MongoClient("mongodb://demouser1:password@35.162.84.93/?authSource=close_loop_validation")
print(client.list_databases())
