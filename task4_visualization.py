# task4_visualization.py
# TrendPulse Project - Task 4
# Visualize trend data using charts

import pandas as pd
import matplotlib.pyplot as plt
import os


def main():

    csv_path = "data/trends_cleaned.csv"

    if not os.path.exists(csv_path):
        print("CSV file not found. Run task2_data_processing.py first.")
        return

    # Load data
    df = pd.read_csv(csv_path)

    # Create plots folder
    os.makedirs("plots", exist_ok=True)

    # -------- Chart 1: Stories per Category --------
    category_counts = df["category"].value_counts()

    plt.figure()
    category_counts.plot(kind="bar")
    plt.title("Number of Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")

    chart1_path = "plots/stories_per_category.png"
    plt.savefig(chart1_path)
    plt.close()

    # -------- Chart 2: Average Score per Category --------
    avg_scores = df.groupby("category")["score"].mean()

    plt.figure()
    avg_scores.plot(kind="bar")
    plt.title("Average Score per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Score")

    chart2_path = "plots/average_score_per_category.png"
    plt.savefig(chart2_path)
    plt.close()

    # -------- Chart 3: Average Comments per Category --------
    avg_comments = df.groupby("category")["num_comments"].mean()

    plt.figure()
    avg_comments.plot(kind="bar")
    plt.title("Average Comments per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Comments")

    chart3_path = "plots/average_comments_per_category.png"
    plt.savefig(chart3_path)
    plt.close()

    print("Charts created successfully:")
    print(chart1_path)
    print(chart2_path)
    print(chart3_path)


if __name__ == "__main__":
    main()
