# task1_data_collection.py
# TrendPulse Project - Task 1
# Fetch trending stories from HackerNews API and categorise them

import requests
import json
import time
import os
from datetime import datetime

# Base API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header for API requests
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords dictionary
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Maximum stories per category
MAX_PER_CATEGORY = 25


def categorize_title(title):
    """
    Assign a category based on keyword matching in the title.
    Returns category name or None if no keyword matched.
    """
    title_lower = title.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in title_lower:
                return category

    return None


def fetch_top_story_ids():
    """
    Fetch the top story IDs from HackerNews API.
    """
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return []


def fetch_story(story_id):
    """
    Fetch a single story by ID.
    """
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def main():

    story_ids = fetch_top_story_ids()

    collected = []
    category_counts = {cat: 0 for cat in categories}

    for story_id in story_ids:

        # Stop once all categories reach the limit
        if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
            break

        story = fetch_story(story_id)

        if not story or "title" not in story:
            continue

        title = story["title"]

        category = categorize_title(title)

        if not category:
            continue

        if category_counts[category] >= MAX_PER_CATEGORY:
            continue

        # Extract required fields
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().isoformat()
        }

        collected.append(story_data)
        category_counts[category] += 1

        # Sleep once per category completion
        if category_counts[category] == MAX_PER_CATEGORY:
            time.sleep(2)

    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)

    # Create filename with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save data
    with open(filename, "w") as f:
        json.dump(collected, f, indent=4)

    print(f"Collected {len(collected)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
