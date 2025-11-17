# ----- README -----
"""
Required installations:
    pip install fastapi uvicorn

Run the server:
    uvicorn MoodLogger:app --reload
"""
# NOTE: I used local JSON as this is a simple class project. For a larger scale project, you may consider a database.

from fastapi import FastAPI, Request
from typing import Dict, List, Any
import json
import uuid
import os

app = FastAPI()
file_path = "mood_log.json"

# Lea, you can rewrite this as you desire! I was just trying to accomplish your "average mood" requirement.
mood_dictionary = {
    "positive": ["happy", "excited", "content"],
    "neutral": ["calm", "indifferent", "fine"],
    "negative": ["sad", "angry", "stressed"]
}

# ----- Utility Functions -----
def load_data() -> Dict[str, List[Dict[str, Any]]]:
    """
    Load the mood log data from the JSON file.

    Returns:
        A dictionary mapping user IDs to lists of mood entries.
        Or an empty dictionary if the file does not exist.
    """
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)
    
def save_data(data: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Save the provided data dictionary to disk as JSON.

    Args:
        data: The mood log structure containing all users and entries.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def classify_mood(mood: str) -> str:
    """
    Determine which category a mood belongs to.

    Args:
        mood: The mood string provided by the user.
    Returns:
        The mood category ('positive', 'neutral', 'negative') or 'undefined' if the mood does not match any category.
    """
    for category, moods in mood_dictionary.items():
        if mood in moods:
            return category
    return "undefined" 

# ----- Routes -----
@app.post("/log_mood")
async def log_mood(request: Request) -> Dict[str, Any]:
    """
    Log a new mood entry for a user.

    Body:
        {
            "user_id": str,
            "mood": str,
            "date": str,
            "journal_text": str
        }
    Returns:
        A status and echo of the submitted entry.
    """
    new_entry = await request.json()
    data = load_data()
    user_id = new_entry["user_id"]

    # Ensure the user has an entry list then append the new entry
    entry_record = {
        "entry_id": str(uuid.uuid4()),
        "date": new_entry["date"],
        "mood_type": classify_mood(new_entry["mood"]),
        "mood": new_entry["mood"],
        "journal_text": new_entry["journal_text"]
    }

    user_log = data.setdefault(user_id, [])
    user_log.append(entry_record)

    try:
        save_data(data)
    except Exception as e:
        return {
            "status": "failure",
            "error": f"Failed to write file: {e}"
        }

    return {
        "status": "success", 
        "new_entry": entry_record
    }

@app.get("/get_mood")
async def get_mood(user_id: str) -> Dict[str, Any]:
    """
    Retrieve all mood entries for a user and compute the user's overall mood trend.

    Body:
        {"user_id": str}
    Returns:
        Status, user ID, list of entries, mood analysis, total entries.
    """
    try:
        data = load_data()
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    # Retrieve entries for this user
    user_data = data[user_id]
    total_entries = len(user_data)

    # Count distribution of mood types
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    for entry in user_data:
        mood_type = entry["mood_type"]
        if mood_type in counts:
            counts[mood_type] += 1 

    # Compute ratios
    total = sum(counts.values()) or 1 # Prevent division by 0
    pos_ratio = counts["positive"] / total
    neg_ratio = counts["negative"] / total

    # Determine user's overall mood trend
    if pos_ratio >= 0.7 and pos_ratio > neg_ratio:
        avg = "positive"
    elif pos_ratio >= 0.5 and pos_ratio > neg_ratio:
        avg = "mostly positive"
    elif neg_ratio >= 0.7 and neg_ratio > pos_ratio:
        avg = "negative"
    elif neg_ratio >= 0.5 and neg_ratio > pos_ratio:
        avg = "mostly negative"
    else:
        avg = "neutral"        

    return {
        "status": "success",
        "user_id": user_id,
        "mood_entries": user_data,
        "average_mood": avg,
        "total_entries": total_entries
    }

@app.patch("/update_mood")
async def update_mood(request: Request) -> Dict[str, Any]:
    """
    Update an existing mood entry for a user.

    Body:
        {
            "user_id": str,
            "entry_id": str,
            "mood": str,
            "journal_text": str
        }
    Returns:
        Status and updated entry data.
    """
    update_info = await request.json()
    user_id = update_info["user_id"]
    entry_id = update_info["entry_id"]

    try:
        data = load_data()
    except Exception as e:
        return {
            "status": "failure",
            "error": f"Failed to read file: {e}"
        }

    # Get list of entries for user
    user_data = data.get(user_id, [])
    updated_entry = None

    # Locate and update the target entry
    for entry in user_data:
        if entry["entry_id"] == entry_id:
            entry["mood"] = update_info["mood"]
            entry["mood_type"] = classify_mood(update_info["mood"])
            entry["journal_text"] = update_info["journal_text"]
            updated_entry = entry
            break    

    if not updated_entry:
        return {
            "status": "failure",
            "error": "Entry not found"
        }
    
    try:
        save_data(data)
    except Exception as e:
        return {
            "status": "failure",
            "error": f"Failed to write file: {e}"
        }

    return {
        "status": "success", 
        "updated_entry": updated_entry
    }

@app.delete("/delete_mood")
async def delete_mood(request: Request) -> Dict[str, Any]:
    """
    Delete a mood entry for a given user.

    Body:
        {
            "user_id": str,
            "entry_id": str
        }
    Returns:
        Status message.
    """
    delete_info = await request.json()
    user_id = delete_info["user_id"]
    entry_id = delete_info["entry_id"]

    try:
        data = load_data()
    except Exception as e:
        return {
            "status": "failure",
            "error": f"Failed to read file: {e}"
        }

    # Filter out the entry to be removed
    user_data = data.get(user_id, [])
    new_user_data = [entry for entry in user_data if entry["entry_id"] != entry_id]
    data[user_id] = new_user_data

    try:
        save_data(data)
    except Exception as e:
        return {
            "status": "failure",
            "error": f"Failed to write file: {e}"
        }

    return {"status": "success"}
