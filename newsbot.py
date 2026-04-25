import feedparser
import anthropic
import requests
import json
import hashlib
import os
import time
import re
from datetime import datetime, timezone
import time as time_module
from config import (
    WP_URL, WP_USERNAME, WP_APP_PASSWORD,
    RSS_FEEDS, MAX_ARTICLES_PER_RUN
)

# GitHub Actions'dan env variable olarak al, yoksa config'den al
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
WP_URL = os.environ.get("WP_URL", WP_URL)
WP_USERNAME = os.environ.get("WP_USERNAME", WP_USERNAME)
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", WP_APP_PASSWORD)

SEEN_FILE = "seen_articles.json"
CATEGORY_CACHE = {}

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def get_or_create_category(category_name):
    if category_name in CATEGORY_CACHE:
        return CATEGORY_CACHE[category_name]

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/categories",
        params={"search": category_name},
        auth=(WP_USERNAME, WP_APP_PASSWORD), verify=False
    )

    if response.status_code == 200:
        for cat in response.json():
            if cat["name"].lower() == category_name.lower():
                CATEGORY_CACHE[category_name] = cat["id"]
                return cat["id"]

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/categories",
        json={"name": category_name},
        auth=(WP_USERNAME, WP_APP_PASSWORD), verify=False
    )

    if response.status_code == 201:
        cat_id = response.json()["id"]
        CATEGORY_CACHE[category_name] = cat_id
        print(f"📁 Kategori oluşturuldu: {category_name} (ID: {cat_id})")
        return cat_id

    return None

def extract_image_url(entry):
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            if media.get("type", "").startswith("image"):
                return media.get("url")

    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")

    if hasattr(entry, "enclosures") and entry.enclosures:
        for enc in entry.enclosures:
            if enc.get("type", "").startswith("image"):
                return enc.get("href") or enc.get("url")

    content = entry.get("summary", "")
    if entry.get("content"):
        content += entry.get("content", [{}])[0].get("value", "")
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    if img_match:
        return img_match.group(1)

    return None

def upload_image_to_wordpress(image_url):
    try:
        img_response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if img_response.status_code != 200:
            return None

        content_type = img_response.headers.get("Content-Type", "image/jpeg")
        ext = "jpg"
        if "png" in content_type: ext = "png"
        elif "gif" in content_type: ext = "gif"
        elif "webp" in content_type: ext = "webp"

        filename = f"news_{hashlib.md5(image_url.encode()).hexdigest()[:8]}.{ext}"

        response = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": content_type,
            },
            data=img_response.content,
            auth=(WP_USERNAME, WP_APP_PASSWORD), verify=False
        )

        if response.status_code == 201:
            media_id = response.json().get("id")
            print(f"🖼️  Resim yüklendi (ID: {media_id})")
            return media_id
        return None

    except Exception as e:
        print(f"⚠️  Resim hatası: {e}")
        return None

def fetch_articles():
    articles = []
    for feed_config in RSS_FEEDS:
        url = feed_config["url"]
        category = feed_config["category"]
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    import time as t
                    if t.time() - t.mktime(published) > 86400:
                        continue
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "link": entry.get("link", ""),
                    "image_url": extract_image_url(entry),
                    "category": category,
                    "id": hashlib.md5(entry.get("link", "").encode()).hexdigest()
                })
        except Exception as e:
            print(f"RSS hatası ({url}): {e}")
    return articles

def rewrite_article(title, summary, category):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Read the following {category} news headline and summary, understand it fully.
Then rewrite it completely in your own words in English.
Make it fluent, engaging, and easy to read.

Return in this exact format:
TITLE: [new title here]
TAGS: [5-8 comma separated keywords/tags]
CONTENT:
[2-3 paragraphs of article body]

Original headline: {title}
Original summary: {summary}"""
        }]
    )

    return message.content[0].text

def post_to_wordpress(title, content, category_name, media_id=None):
    # Parse structured response
    wp_title = title
    wp_content = content
    tags = []

    lines = content.strip().split("\n")
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith("TITLE:"):
            wp_title = line.replace("TITLE:", "").strip()
        elif line.startswith("TAGS:"):
            tags = [t.strip() for t in line.replace("TAGS:", "").split(",") if t.strip()]
        elif line.startswith("CONTENT:"):
            content_start = i + 1

    if content_start:
        wp_content = "\n".join(lines[content_start:]).strip()

    if not wp_title: wp_title = title
    if not wp_content: wp_content = content

    # Kategori ID al
    cat_id = get_or_create_category(category_name)

    # Tag ID'lerini al veya oluştur
    tag_ids = []
    for tag in tags:
        try:
            r = requests.get(f"{WP_URL}/wp-json/wp/v2/tags", params={"search": tag}, auth=(WP_USERNAME, WP_APP_PASSWORD), verify=False)
            found = [t for t in r.json() if t["name"].lower() == tag.lower()]
            if found:
                tag_ids.append(found[0]["id"])
            else:
                r2 = requests.post(f"{WP_URL}/wp-json/wp/v2/tags", json={"name": tag}, auth=(WP_USERNAME, WP_APP_PASSWORD), verify=False)
                if r2.status_code == 201:
                    tag_ids.append(r2.json()["id"])
        except:
            pass

    data = {
        "title": wp_title,
        "content": wp_content,
        "status": "publish",
    }

    if cat_id:
        data["categories"] = [cat_id]
    if tag_ids:
        data["tags"] = tag_ids
    if media_id:
        data["featured_media"] = media_id

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        json=data,
        auth=(WP_USERNAME, WP_APP_PASSWORD), verify=False
    )

    if response.status_code == 201:
        print(f"✅ [{category_name}] Yayınlandı: {wp_title}")
        return True
    else:
        print(f"❌ WordPress hatası: {response.status_code} - {response.text[:200]}")
        return False

def run():
    print(f"\n🔄 Çalışıyor: {datetime.now().strftime('%H:%M:%S')}")

    seen = load_seen()
    articles = fetch_articles()

    new_articles = [a for a in articles if a["id"] not in seen]

    processed_titles = set()
    unique_articles = []
    for a in new_articles:
        title_key = a["title"][:40].lower()
        if title_key not in processed_titles:
            if a.get("image_url"):
                unique_articles.append(a)
            processed_titles.add(title_key)

    print(f"📰 {len(new_articles)} yeni haber, {len(unique_articles)} benzersiz")

    # Kategori kotaları - minimum kaç haber yayınlansın
    category_quotas = {
        "Sports": 2,
        "Politics": 2,
        "US News": 2,
        "Business": 1,
        "Technology": 1,
        "Health": 1,
        "Entertainment": 1,
    }
    category_counts = {k: 0 for k in category_quotas}
    count = 0

    # Önce kotası olan kategorileri doldur
    priority_articles = []
    remaining_articles = []
    for a in unique_articles:
        cat = a["category"]
        if cat in category_counts and category_counts[cat] < category_quotas.get(cat, 0):
            priority_articles.append(a)
            category_counts[cat] += 1
        else:
            remaining_articles.append(a)

    ordered_articles = priority_articles + remaining_articles

    for article in ordered_articles:
        if count >= MAX_ARTICLES_PER_RUN:
            break

        try:
            print(f"✍️  [{article['category']}] {article['title'][:50]}...")
            rewritten = rewrite_article(article["title"], article["summary"], article["category"])

            media_id = None
            if article.get("image_url"):
                media_id = upload_image_to_wordpress(article["image_url"])

            success = post_to_wordpress(article["title"], rewritten, article["category"], media_id)
            if success:
                seen.add(article["id"])
                count += 1
                time.sleep(2)

        except Exception as e:
            print(f"Hata: {e}")

    save_seen(seen)
    print(f"✅ Bitti. {count} haber yayınlandı.")

if __name__ == "__main__":
    run()
