import requests
import os
from django.conf import settings
import time

CACHE = {
    "data": None,
    "timestamp": 0
}

CACHE_EXPIRY = 60  # seconds



API_KEY = settings.API_KEY
API_HOST = settings.API_HOST


def fetch_live_match(match_id=None):
    global CACHE

    now = time.time()

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    live_url = f"https://{API_HOST}/matches/v1/live"
    live_response = requests.get(live_url, headers=headers)

    # 🔴 If API fails (quota exceeded or other error)
    if live_response.status_code != 200:

        # ✅ If cached data exists, return last known good data
        if CACHE["data"]:
            return CACHE["data"]

        # 🧪 If no cache, return demo data
        return {
            "match_state": "Demo Mode",
            "status": "API quota exceeded - showing demo data",
            "team1": "England",
            "team2": "Italy",
            "real_score": "England 202/7 (19.6)",
            "current_score": 73,
            "overs_completed": 8.3,
            "wickets_lost": 3,
            "target": 203
        }

    # 🟢 If API succeeds
    live_data = live_response.json()

    try:
        match = live_data["typeMatches"][0]["seriesMatches"][0]["seriesAdWrapper"]["matches"][0]

        match_info = match["matchInfo"]
        match_score = match.get("matchScore", {})

        match_state = match_info["state"]
        status = match_info["status"]

        team1 = match_info["team1"]["teamName"]
        team2 = match_info["team2"]["teamName"]

        first_innings = match_score.get("team1Score", {}).get("inngs1", {})
        real_score = f"{team1} {first_innings.get('runs', 0)}/{first_innings.get('wickets', 0)} ({first_innings.get('overs', 0)})"

        second_innings = match_score.get("team2Score", {}).get("inngs1", None)

        if not second_innings:
            response_data = {
                "match_state": match_state,
                "status": status,
                "team1": team1,
                "team2": team2,
                "real_score": real_score,
                "message": "Second innings not started yet"
            }

            CACHE["data"] = response_data
            CACHE["timestamp"] = now
            return response_data

        current_score = second_innings.get("runs", 0)
        wickets_lost = second_innings.get("wickets") or second_innings.get("wkts", 0)
        overs_completed = float(second_innings.get("overs", 0))

        import re
        target_match = re.search(r"need (\d+) runs", status)
        target = current_score + int(target_match.group(1)) if target_match else 0

        response_data = {
            "match_state": match_state,
            "status": status,
            "team1": team1,
            "team2": team2,
            "real_score": real_score,
            "current_score": current_score,
            "overs_completed": overs_completed,
            "wickets_lost": wickets_lost,
            "target": target
        }

        # ✅ Save successful response in cache
        CACHE["data"] = response_data
        CACHE["timestamp"] = now

        return response_data

    except Exception as e:
        return {"error": f"Live parsing failed: {str(e)}"}
