"""
Mood Recommendation Microservice
Required installations:
    pip install fastapi uvicorn

Run the server:
    uvicorn MoodRecommendationService:app --reload --port 8003
"""

from fastapi import FastAPI, Request
from typing import Dict, Any

app = FastAPI()

# ---- Coping strategies & resource lists ----
coping_strategies = {
    "very_low": [
        "Try slow deep breathing for 2 minutes",
        "Take a short walk outside",
        "Drink a glass of water and rest briefly"
    ],
    "low": [
        "Write a short reflection about how you're feeling",
        "Listen to calming music",
        "Do a simple grounding exercise (5-4-3-2-1)"
    ],
    "neutral": [
        "Take a moment to stretch your body",
        "Set a small goal for the next hour",
        "Practice mindful breathing"
    ],
    "positive": [
        "Celebrate things that went well today",
        "Share something good with a friend",
        "Do an activity you enjoy"
    ],
    "very_positive": [
        "Reflect on what contributed to your good mood today",
        "Try a creative activity like doodling or journaling",
        "Spread kindness to someone else"
    ]
}

osu_resources = [
    "CAPS Counseling – osu.edu/caps",
    "Wellness Coaching – Dixon Recreation Center",
    "OSU Student Peer Support Network",
    "Mind Spa – OSU Counseling Center"
]


# -------- ROUTES --------
@app.post("/recommendations")
async def recommendations(request: Request) -> Dict[str, Any]:
    """
    Provide mood-based coping suggestions and OSU resources.

    Body:
        {
            "mood_score": 1–5,
            "user_id": "optional"
        }

    Returns:
        Coping strategies and (if low) campus mental health resources.
    """
    body = await request.json()
    mood_score = body.get("mood_score")

    print(f"[MoodRecommendationService] Recommendation request received. Score = {mood_score}")

    if mood_score is None or not isinstance(mood_score, int):
        return {
            "status": "error",
            "message": "mood_score must be an integer between 1 and 5."
        }

    # ---- Determine category based on score ----
    if mood_score == 1:
        category = "very_low"
    elif mood_score == 2:
        category = "low"
    elif mood_score == 3:
        category = "neutral"
    elif mood_score == 4:
        category = "positive"
    else:  # mood_score == 5
        category = "very_positive"

    base_recommendations = coping_strategies[category]

    response = {
        "status": "success",
        "mood_score": mood_score,
        "category": category,
        "coping_strategies": base_recommendations
    }

    # ---- If mood is low, add OSU resources ----
    if mood_score <= 2:
        response["osu_resources"] = osu_resources

    return response
