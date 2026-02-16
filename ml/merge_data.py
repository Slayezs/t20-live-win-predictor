import os
import yaml
import pandas as pd


def parse_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    match_id = os.path.basename(filepath).replace(".yaml", "")
    rows = []

    if "innings" not in data:
        return None

    winner = None
    if "info" in data and "outcome" in data["info"]:
        outcome = data["info"]["outcome"]
        if "winner" in outcome:
            winner = outcome["winner"]

    for inning_index, inning in enumerate(data["innings"]):
        inning_name = list(inning.keys())[0]
        deliveries = inning[inning_name]["deliveries"]
        batting_team = inning[inning_name]["team"]

        for delivery in deliveries:
            for ball, details in delivery.items():
                over = int(float(ball))
                ball_number = int((float(ball) % 1) * 10)

                total_runs = details["runs"]["total"]
                is_wicket = 1 if "wickets" in details else 0

                rows.append({
                    "match_id": match_id,
                    "inning": inning_index + 1,
                    "over": over,
                    "ball": ball_number,
                    "batting_team": batting_team,
                    "total_runs": total_runs,
                    "is_wicket": is_wicket,
                    "winner": winner
                })

    return pd.DataFrame(rows)


def parse_folder(folder_path):
    all_data = []

    files = [f for f in os.listdir(folder_path) if f.endswith(".yaml")]

    print(f"Total YAML files found: {len(files)}")

    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        df = parse_yaml_file(file_path)

        if df is not None:
            all_data.append(df)

        if i % 200 == 0:
            print(f"Processed {i} files...")

    return pd.concat(all_data, ignore_index=True)


if __name__ == "__main__":
    df = parse_folder("data/t20s")
    df.to_csv("data/ball_by_ball.csv", index=False)

    print("ball_by_ball.csv created successfully.")
