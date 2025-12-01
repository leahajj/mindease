"""
Mood Summary Microservice
Required installations:
    pip install fastapi uvicorn

Run the server:
    uvicorn MoodSummaryService:app --reload --port 8001
"""

from fastapi import FastAPI
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json
import os

app = FastAPI()
file_path = "mood_log.json"

# -------- Utility Functions --------
def load_data() -> Dict[str, List[Dict[str, Any]]]:
    """Load all mood logs."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)


def filter_by_date(entries: List[Dict[str, Any]], target_date: str) -> List[Dict[str, Any]]:
    """Return entries that match a specific date."""
    return [e for e in entries if e["date"] == target_date]


# --------- ROUTES ---------
@app.get("/daily_summary")
async def daily_summary(user_id: str, date: str):
    """
    Return the user's daily mood summary for a given date.
    Example: /daily_summary?user_id=123&date=2025-12-01
    """
    print(f"[MoodSummaryService] DAILY summary request for user {user_id} on date {date}")

    data = load_data()
    entries = data.get(user_id, [])

    todays_entries = filter_by_date(entries, date)

    if not todays_entries:
        return {
            "status": "no_entries",
            "message": "No mood entries found for this date."
        }

    moods = [e["mood"] for e in todays_entries]
    avg_mood_type = todays_entries[-1]["mood_type"]
    most_recent = todays_entries[-1]["mood"]

    return {
        "status": "success",
        "user_id": user_id,
        "date": date,
        "total_entries": len(todays_entries),
        "most_recent_mood": most_recent,
        "average_mood_type": avg_mood_type,
        "moods": moods
    }


@app.get("/weekly_summary")
async def weekly_summary(user_id: str):
    """
    Return a 7-day breakdown of mood entries.
    Example: /weekly_summary?user_id=123
    """
    print(f"[MoodSummaryService] WEEKLY summary request for user {user_id}")

    data = load_data()
    entries = data.get(user_id, [])

    if not entries:
        return {"status": "no_entries", "message": "No mood logs found for this user."}

    # Build last 7 days
    today = datetime.now().date()
    week_data = {}

    for i in range(7):
        day = (today - timedelta(days=i)).isoformat()
        filtered = filter_by_date(entries, day)
        week_data[day] = {
            "count": len(filtered),
            "moods": [e["mood"] for e in filtered]
        }

    return {
        "status": "success",
        "user_id": user_id,
        "weekly_data": week_data
    }
