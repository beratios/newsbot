# ============================================================
# BURAYA KENDİ BİLGİLERİNİ GİR
# ============================================================

ANTHROPIC_API_KEY = "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"        # Yeni API key'in

WP_URL = "https://monarqscreen.com"     # Site URL'in
WP_USERNAME = "berattios"                    # WordPress kullanıcı adın
WP_APP_PASSWORD = "Berat1995****"      # WordPress uygulama şifresi (aşağıda nasıl oluşturulur yazar)

# ============================================================
# HABER KAYNAKLARI
# ============================================================

RSS_FEEDS = [
    # --- US NEWS ---
    {"url": "http://rss.cnn.com/rss/cnn_us.rss",                        "category": "US News"},
    {"url": "http://rss.foxnews.com/fn/latest/feed/0/fnc/us",           "category": "US News"},
    {"url": "https://feeds.apnews.com/rss/apf-usnews",                  "category": "US News"},

    # --- POLITICS ---
    {"url": "http://rss.cnn.com/rss/cnn_allpolitics.rss",               "category": "Politics"},
    {"url": "http://feeds.foxnews.com/foxnews/politics",                 "category": "Politics"},
    {"url": "https://feeds.apnews.com/rss/apf-politics",                 "category": "Politics"},

    # --- HEALTH ---
    {"url": "http://rss.cnn.com/rss/edition_health.rss",                "category": "Health"},
    {"url": "http://feeds.foxnews.com/foxnews/health",                   "category": "Health"},

    # --- TECHNOLOGY ---
    {"url": "http://rss.cnn.com/rss/edition_technology.rss",            "category": "Technology"},
    {"url": "https://feeds.feedburner.com/TechCrunch/",                  "category": "Technology"},

    # --- SPORTS ---
    {"url": "http://rss.cnn.com/rss/edition_sport.rss",                 "category": "Sports"},
    {"url": "https://www.espn.com/espn/rss/news",                        "category": "Sports"},

    # --- ENTERTAINMENT ---
    {"url": "http://rss.cnn.com/rss/edition_entertainment.rss",         "category": "Entertainment"},
    {"url": "http://feeds.foxnews.com/foxnews/entertainment",            "category": "Entertainment"},

    # --- BUSINESS ---
    {"url": "http://rss.cnn.com/rss/edition_business.rss",              "category": "Business"},
    {"url": "https://feeds.apnews.com/rss/apf-business",                 "category": "Business"},
]

# Kaç saatte bir çalışsın
INTERVAL_HOURS = 1

# Her çalışmada kaç haber işlensin (toplam)
MAX_ARTICLES_PER_RUN = 10
