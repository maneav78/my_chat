import requests
from datetime import datetime

url = "http://localhost:5000/api/send_message" 
payload = {
    "message": "This is a test message from CI pipeline.",
    "name": "CI Bot",
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
