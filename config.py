import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
WP_URL = os.environ.get("WP_URL", "https://monarqscreen.com")
WP_USERNAME = os.environ.get("WP_USERNAME", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")

RSS_FEEDS = [
    {"url": "http://rss.cnn.com/rss/cnn_us.rss",                       "category": "US News"},
    {"url": "http://rss.foxnews.com/fn/latest/feed/0/fnc/us",          "category": "US News"},
    {"url": "https://feeds.apnews.com/rss/apf-usnews",                 "category": "US News"},
    {"url": "http://rss.cnn.com/rss/cnn_allpolitics.rss",              "category": "Politics"},
    {"url": "http://feeds.foxnews.com/foxnews/politics",                "category": "Politics"},
    {"url": "https://feeds.apnews.com/rss/apf-politics",               "category": "Politics"},
    {"url": "http://rss.cnn.com/rss/edition_health.rss",               "category": "Health"},
    {"url": "http://feeds.foxnews.com/foxnews/health",                  "category": "Health"},
    {"url": "http://rss.cnn.com/rss/edition_technology.rss",           "category": "Technology"},
    {"url": "https://feeds.feedburner.com/TechCrunch/",                 "category": "Technology"},
    {"url": "http://rss.cnn.com/rss/edition_sport.rss",                "category": "Sports"},
    {"url": "https://www.espn.com/espn/rss/news",                       "category": "Sports"},
    {"url": "http://rss.cnn.com/rss/edition_entertainment.rss",        "category": "Entertainment"},
    {"url": "http://feeds.foxnews.com/foxnews/entertainment",           "category": "Entertainment"},
    {"url": "http://rss.cnn.com/rss/edition_business.rss",             "category": "Business"},
    {"url": "https://feeds.apnews.com/rss/apf-business",               "category": "Business"},
]

INTERVAL_HOURS = 1
MAX_ARTICLES_PER_RUN = 10
