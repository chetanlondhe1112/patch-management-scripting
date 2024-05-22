import requests
import json

# Define the URL of your FastAPI endpoint
url = 'http://127.0.0.1:8000/rabbitmq-data'

# Define the data you want to send (assuming it's in JSON format)
data = {
    "key1": "value1",
    "key2": "value2"
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the headers to specify the content type as JSON
headers = {'Content-Type': 'application/json'}

# Make the HTTP POST request
response = requests.post(url, data=json_data, headers=headers)
print(response)
# Check the response
if response.status_code == 200:
    print("Data sent successfully to FastAPI endpoint.")
else:
    print(f"Failed to send data to FastAPI endpoint. Status code: {response.status_code}")
    print(response.text)
