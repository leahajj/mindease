"""
Mood Trend Analysis Microservice
Required installations:
    pip install fastapi uvicorn

Run the server:
    uvicorn MoodTrendAnalysisService:app --reload --port 8002
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


def convert_mood_to_score(mood_type: str) -> int:
    """
    Convert mood categories into numeric values for trend analysis.
    Higher = more positive.
    """
    mapping = {
        "positive": 3,
        "mostly positive": 2,
        "neutral": 1,
        "mostly negative": -1,
        "negative": -2
    }
    return mapping.get(mood_type, 0)  # default for undefined


# --------- ROUTES ---------
@app.get("/trend")
async def trend(user_id: str):
    """
    Detect long-term mood trends using the last 14 days of logs.
    Example: /trend?user_id=123
    """
    print(f"[MoodTrendAnalysisService] TREND analysis request for user {user_id}")

    data = load_data()
    entries = data.get(user_id, [])

    if not entries:
        return {"status": "no_entries", "message": "No mood logs found for this user."}

    # Convert entries to (date, score) pairs
    daily_scores = {}
    today = datetime.now().date()

    # Look back 14 days
    for i in range(14):
        day = (today - timedelta(days=i)).isoformat()
        moods_on_day = [e["mood_type"] for e in entries if e["date"] == day]

        if moods_on_day:
            # Average score for the day
            scores = [convert_mood_to_score(m) for m in moods_on_day]
            avg_score = sum(scores) / len(scores)
            daily_scores[day] = avg_score

    if len(daily_scores) < 3:
        return {
            "status": "insufficient_data",
            "message": "Not enough data to determine trend."
        }

    # Sort by date (oldest first)
    sorted_days = sorted(daily_scores.keys())
    ordered_scores = [daily_scores[d] for d in sorted_days]

    # Compare early vs late averages
    first_half = ordered_scores[:len(ordered_scores) // 2]
    second_half = ordered_scores[len(ordered_scores) // 2:]

    avg_first = sum(first_half) / len(first_half)
    avg_second = sum(second_half) / len(second_half)

    # Determine trend
    if avg_second - avg_first > 0.4:
        trend_result = "increasing"
    elif avg_first - avg_second > 0.4:
        trend_result = "decreasing"
    else:
        trend_result = "stable"

    return {
        "status": "success",
        "user_id": user_id,
        "trend": trend_result,
        "daily_scores": daily_scores,
        "first_half_avg": avg_first,
        "second_half_avg": avg_second
    }
