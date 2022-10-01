import requests
import uuid

r = requests.post(url='http://localhost:5000/get_data', json={'job_id': str(uuid.uuid4())})
print(r)
