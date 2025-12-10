import requests
import base64
import json
import os

API_URL = "http://localhost:8000/recognize"
IMAGE_PATH = "test_img.jpg"

if not os.path.exists(IMAGE_PATH):
    print(f"Error: {IMAGE_PATH} not found.")
    exit()

with open(IMAGE_PATH, "rb") as image_file:
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')

payload = {
    "image_base64": base64_string
}

try:
    print(f"Sending request to {API_URL}...")
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        print("\n✅ Success!")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")