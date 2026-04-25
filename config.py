import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
WP_URL = os.environ.get("WP_URL", "https://monarqscreen.com")
WP_USERNAME = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")

RSS_FEEDS = [
    # --- US NEWS ---
    {"url": "https://feeds.apnews.com/rss/apf-usnews",                      "category": "US News"},
    {"url": "https://moxie.foxnews.com/google-publisher/us.xml",            "category": "US News"},
    {"url": "https://feeds.nbcnews.com/nbcnews/public/news",                "category": "US News"},

    # --- POLITICS ---
    {"url": "https://feeds.apnews.com/rss/apf-politics",                    "category": "Politics"},
    {"url": "https://moxie.foxnews.com/google-publisher/politics.xml",      "category": "Politics"},

    # --- HEALTH ---
    {"url": "https://feeds.apnews.com/rss/apf-Health",                      "category": "Health"},
    {"url": "https://moxie.foxnews.com/google-publisher/health.xml",        "category": "Health"},

    # --- TECHNOLOGY ---
    {"url": "https://feeds.apnews.com/rss/apf-technology",                  "category": "Technology"},
    {"url": "https://feeds.feedburner.com/TechCrunch/",                     "category": "Technology"},

    # --- SPORTS ---
    {"url": "https://feeds.apnews.com/rss/apf-sports",                      "category": "Sports"},
    {"url": "https://www.espn.com/espn/rss/news",                           "category": "Sports"},

    # --- ENTERTAINMENT ---
    {"url": "https://feeds.apnews.com/rss/apf-entertainment",               "category": "Entertainment"},
    {"url": "https://moxie.foxnews.com/google-publisher/entertainment.xml", "category": "Entertainment"},

    # --- BUSINESS ---
    {"url": "https://feeds.apnews.com/rss/apf-business",                    "category": "Business"},
]

INTERVAL_HOURS = 1
MAX_ARTICLES_PER_RUN = 10
