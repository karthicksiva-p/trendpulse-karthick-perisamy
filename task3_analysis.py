# task3_analysis.py
# TrendPulse Project - Task 3
# Analyze cleaned trend data

import pandas as pd
import numpy as np
import os


def main():

    csv_path = "data/trends_cleaned.csv"

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print("CSV file not found. Run task2_data_processing.py first.")
        return

    # Load CSV into pandas DataFrame
    df = pd.read_csv(csv_path)

    print("\nTotal stories:", len(df))

    # Average score
    avg_score = np.mean(df["score"])
    print("Average score:", round(avg_score, 2))

    # Average number of comments
    avg_comments = np.mean(df["num_comments"])
    print("Average comments:", round(avg_comments, 2))

    # Count stories per category
    print("\nStories per category:")
    category_counts = df["category"].value_counts()
    print(category_counts)

    # Highest scoring story
    top_score_story = df.loc[df["score"].idxmax()]
    print("\nTop scoring story:")
    print(top_score_story["title"])
    print("Score:", top_score_story["score"])

    # Most commented story
    top_comments_story = df.loc[df["num_comments"].idxmax()]
    print("\nMost commented story:")
    print(top_comments_story["title"])
    print("Comments:", top_comments_story["num_comments"])


if __name__ == "__main__":
    main()
