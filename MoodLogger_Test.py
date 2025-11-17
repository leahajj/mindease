# ----- README -----
"""
Required installations:
    pip install requests

Ensure MoodLogger.py is running, then run this file!
"""

import requests
import uuid

base_url = "http://127.0.0.1:8000"
user_id = str(uuid.uuid4())

# ----- /log_mood -----
print("Testing /log_mood")
response = requests.post(f"{base_url}/log_mood", json={
    "user_id": user_id,
    "mood": "happy",
    "date": "2025-11-16",
    "journal_text": "Today was good!"
})
print(response.json(), "\n")
entry_id = response.json().get("new_entry", {}).get("entry_id") 

# ----- /get_mood -----
print("Testing /get_mood")
response = requests.get(f"{base_url}/get_mood", params={"user_id": user_id})
print(response.json(), "\n")

# ----- /update_mood -----
if entry_id:
    print("Testing /update_mood")
    response = requests.patch(f"{base_url}/update_mood", json={
        "user_id": user_id,
        "entry_id": entry_id,
        "mood": "stressed",
        "journal_text": "Today was bad."
    })
    print(response.json(), "\n")

# ----- /delete_mood -----
if entry_id:
    print("Testing /delete_mood")
    response = requests.delete(f"{base_url}/delete_mood", json={
        "user_id": user_id,
        "entry_id": entry_id
    })
    print(response.json(), "\n")

# ----- /get_mood after deletion -----
print("Testing /get_mood after deletion")
response = requests.get(f"{base_url}/get_mood", params={"user_id": user_id})
print(response.json(), "\n")
