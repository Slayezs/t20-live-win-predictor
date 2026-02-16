import pandas as pd


def prepare_training_data():
    df = pd.read_csv("data/ball_by_ball.csv")

    # Keep only second innings
    df = df[df["inning"] == 2]

    # Create result column
    df["result"] = (df["batting_team"] == df["winner"]).astype(int)

    df.to_csv("data/second_innings.csv", index=False)

    print("Second innings dataset created.")


if __name__ == "__main__":
    prepare_training_data()
