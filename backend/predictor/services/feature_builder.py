def build_features(data):
    current_score = data["current_score"]
    overs_completed = data["overs_completed"]
    wickets_lost = data["wickets_lost"]
    target = data["target"]

    # Convert overs (e.g., 15.2 means 15 overs + 2 balls)
    full_overs = int(overs_completed)
    balls = int(round((overs_completed - full_overs) * 10))

    balls_completed = full_overs * 6 + balls
    balls_left = 120 - balls_completed

    runs_left = target - current_score

    current_run_rate = current_score / (balls_completed / 6 + 0.01)
    required_run_rate = runs_left / (balls_left / 6 + 0.01)

    wickets_remaining = 10 - wickets_lost

    return {
        "current_score": current_score,
        "wickets_lost": wickets_lost,
        "balls_left": balls_left,
        "runs_left": runs_left,
        "current_run_rate": current_run_rate,
        "required_run_rate": required_run_rate,
        "wickets_remaining": wickets_remaining
    }
