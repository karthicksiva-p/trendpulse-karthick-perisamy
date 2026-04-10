# task2_data_processing.py
# TrendPulse Project - Task 2
# Load JSON data from Task 1, clean it, and save as CSV

import os
import glob
import json
import pandas as pd


def find_latest_json():
    """
    Find the most recent trends JSON file in the data folder.
    """
    files = glob.glob("data/trends_*.json")

    if not files:
        print("No trends JSON file found. Run task1_data_collection.py first.")
        return None

    return max(files)


def main():

    # Find latest JSON file
    json_file = find_latest_json()

    if not json_file:
        return

    print(f"Loading data from {json_file}")

    # Load JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Convert JSON to pandas DataFrame
    df = pd.DataFrame(data)

    print(f"Original records: {len(df)}")

    # Remove duplicate posts
    df = df.drop_duplicates(subset="post_id")

    # Fill missing values
    df["score"] = df["score"].fillna(0)
    df["num_comments"] = df["num_comments"].fillna(0)
    df["author"] = df["author"].fillna("unknown")

    # Convert numeric columns
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save cleaned CSV
    csv_path = "data/trends_cleaned.csv"
    df.to_csv(csv_path, index=False)

    print(f"Cleaned records: {len(df)}")
    print(f"CSV saved to {csv_path}")


if __name__ == "__main__":
    main()
