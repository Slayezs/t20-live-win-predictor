import pandas as pd


def create_features():
    df = pd.read_csv("data/second_innings.csv")

    df["current_score"] = df.groupby("match_id")["total_runs"].cumsum()
    df["wickets_lost"] = df.groupby("match_id")["is_wicket"].cumsum()

    df["balls_completed"] = (df["over"] - 1) * 6 + df["ball"]
    df["overs_completed"] = df["balls_completed"] / 6
    df["balls_left"] = 120 - df["balls_completed"]

    # Get target from first innings
    full_data = pd.read_csv("data/ball_by_ball.csv")
    first_innings = full_data[full_data["inning"] == 1]
    first_innings["first_innings_score"] = first_innings.groupby("match_id")["total_runs"].cumsum()

    targets = (
        first_innings.groupby("match_id")["first_innings_score"]
        .max()
        .reset_index()
        .rename(columns={"first_innings_score": "target"})
    )

    df = df.merge(targets, on="match_id", how="left")

    df["runs_left"] = df["target"] - df["current_score"]

    df["current_run_rate"] = df["current_score"] / (df["balls_completed"] / 6 + 0.01)
    df["required_run_rate"] = df["runs_left"] / (df["balls_left"] / 6 + 0.01)

    df["wickets_remaining"] = 10 - df["wickets_lost"]

    df = df[df["balls_left"] > 0]
    # Remove early overs noise
    df = df[df["overs_completed"] >= 5]


    df.to_csv("data/training_data.csv", index=False)

    print("Feature engineering completed.")


if __name__ == "__main__":
    create_features()
