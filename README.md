# MindEase Mood Logging Microservice

This microservice allows the MindEase application to log a user’s mood, retrieve mood history, update existing entries, and delete entries. The service uses a JSON file to store all user mood logs.

-------------------------------------------------------------------

## 1. How to REQUEST Data From This Microservice

Your program can send POST, GET, PATCH, or DELETE requests to:

http://    

Below is the required JSON or URL parameters for each endpoint.

--------------------------------------------------------------------

###  POST `/log_mood`
Logs a new mood entry.

Request JSON body:
```json
{
  "user_id": "abc123",
  "mood": "happy",
  "date": "2025-11-16",
  "journal_text": "Today was good!"
}
```

-------

###  GET `/get_mood`
Retrieves all stored mood entries for a user.

Request (URL Parameters):
```
/get_mood?user_id=abc123
```

-------

###  PATCH `/update_mood`
Updates a specific mood entry.

Request JSON body:
```json
{
  "user_id": "abc123",
  "entry_id": "UUID",
  "mood": "stressed",
  "journal_text": "Feeling overwhelmed."
}
```

-------

### DELETE `/delete_mood`
Deletes a specific mood entry.

Request JSON body:
```json
{
  "user_id": "abc123",
  "entry_id": "UUID"
}
```

-------

## 2. How to RECEIVE Data From This Microservice

All responses are returned in JSON.

-------

###  Response for `/log_mood`
```json
{
  "status": "success",
  "new_entry": {
    "entry_id": "UUID",
    "date": "2025-11-16",
    "mood_type": "positive",
    "mood": "happy",
    "journal_text": "Today was good!"
  }
}
```

-------

### Response for `/get_mood`
```json
{
  "status": "success",
  "user_id": "abc123",
  "mood_entries": [...],
  "average_mood": "mostly positive",
  "total_entries": 3
}
```

-------

### Response for `/update_mood`
```json
{
  "status": "success",
  "updated_entry": {
    "entry_id": "UUID",
    "mood": "stressed",
    "mood_type": "negative",
    "journal_text": "Feeling overwhelmed."
  }
}
```

-------

###  Response for `/delete_mood`
```json
{
  "status": "success"
}
```

-------

## Example Test Program 

```python
import requests
import uuid

base_url = "http://127.0.0.1:8000"
user_id = str(uuid.uuid4())

# log_mood
response = requests.post(f"{base_url}/log_mood", json={
    "user_id": user_id,
    "mood": "happy",
    "date": "2025-11-16",
    "journal_text": "Today was good!"
})
print(response.json())
entry_id = response.json().get("new_entry", {}).get("entry_id")

# get_mood
response = requests.get(f"{base_url}/get_mood", params={"user_id": user_id})
print(response.json())

# update_mood
response = requests.patch(f"{base_url}/update_mood", json={
    "user_id": user_id,
    "entry_id": entry_id,
    "mood": "stressed",
    "journal_text": "Feeling overwhelmed."
})
print(response.json())

# delete_mood
response = requests.delete(f"{base_url}/delete_mood", json={
    "user_id": user_id,
    "entry_id": entry_id
})
print(response.json())
```

-------

## UML Sequence Diagram (Text Version)

```
TestProgram -> MoodLoggerService: POST /log_mood {data}
MoodLoggerService -> FileSystem: save_data()
MoodLoggerService --> TestProgram: JSON response

TestProgram -> MoodLoggerService: GET /get_mood?user_id=...
MoodLoggerService -> FileSystem: load_data()
MoodLoggerService --> TestProgram: JSON response

TestProgram -> MoodLoggerService: PATCH /update_mood {data}
MoodLoggerService -> FileSystem: update_data()
MoodLoggerService --> TestProgram: JSON response

TestProgram -> MoodLoggerService: DELETE /delete_mood {data}
MoodLoggerService -> FileSystem: delete_data()
MoodLoggerService --> TestProgram: JSON response
```

-------

## How to Run This Microservice

1. Install requirements:
```
pip install fastapi uvicorn requests
```

2. Start the microservice:
```
uvicorn MoodLogger:app --reload
```

3. Run the test program:
```
python3 MoodLogger_Test.py
```

---

## Notes

- All communication uses JSON  
- No authentication required  
- Data is saved in `mood_log.json`  
- Moods are automatically labeled positive/neutral/negative  
- Each entry uses a unique `entry_id`  
