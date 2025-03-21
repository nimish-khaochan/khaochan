import feedparser
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsItem

RSS_FEED_URL = "https://example.com/rss"

class Command(BaseCommand):
    help = "Scrapes a general RSS feed and inserts new articles into the database."

    def handle(self, *args, **options):
        self.stdout.write(f"Fetching feed from: {RSS_FEED_URL}")
        feed = feedparser.parse(RSS_FEED_URL)

        if feed.bozo:
            self.stderr.write("Error parsing the feed. Please check the URL or feed structure.")
            return

        # --- 1) Extract top-level publisher info ---
        publisher_name = None
        publisher_logo_url = None

        # feed.feed.title is often the site name
        if hasattr(feed.feed, "title"):
            publisher_name = feed.feed.title

        # feed.feed.image might hold the top-level <image> tag
        # e.g. feed.feed.image.title, feed.feed.image.href or feed.feed.image.url
        if hasattr(feed.feed, "image") and feed.feed.image:
            if hasattr(feed.feed.image, "title"):
                publisher_name = feed.feed.image.title or publisher_name
            if hasattr(feed.feed.image, "href"):
                publisher_logo_url = feed.feed.image.href
            elif hasattr(feed.feed.image, "url"):
                publisher_logo_url = feed.feed.image.url

        entries = feed.entries
        self.stdout.write(f"Found {len(entries)} entries in RSS feed.")

        for entry in entries:
            # Basic fields
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            description = entry.get("description", "").strip()

            # Parse the published date
            published_parsed = entry.get("published_parsed")
            if published_parsed:
                pub_date = datetime.fromtimestamp(time.mktime(published_parsed))
            else:
                pub_date = datetime.now()

            # --- 2) Extract an article image URL (if any) from content:encoded or description ---
            image_url = None

            # Some feeds store the HTML content in content:encoded
            raw_html = entry.get("content", None)
            if raw_html and isinstance(raw_html, list):
                # feedparser might store it as a list of dicts
                # e.g. entry.content[0]["value"]
                raw_html = raw_html[0].get("value", "")
            elif entry.get("content:encoded"):
                # occasionally feedparser might parse it differently
                raw_html = entry["content:encoded"]
            else:
                # fallback to entry.description if no content:encoded
                raw_html = entry.get("description", "")

            if raw_html:
                soup = BeautifulSoup(raw_html, "html.parser")
                first_img = soup.find("img")
                if first_img and first_img.get("src"):
                    image_url = first_img["src"]

            # --- 3) Check for duplicates by link ---
            if NewsItem.objects.filter(source_link=link).exists():
                self.stdout.write(f"Skipping existing article: {title}")
                continue

            # --- 4) Create a new NewsItem ---
            news_item = NewsItem(
                title=title,
                summary=description,
                source_link=link,
                image_url=image_url,  # store the found image
                publisher_name=publisher_name,
                publisher_logo_url=publisher_logo_url,
                date_published=pub_date,
            )
            news_item.save()
            self.stdout.write(f"Saved new article: {title}")

        self.stdout.write("General RSS scraping complete.")
