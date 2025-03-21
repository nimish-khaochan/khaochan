import feedparser
import time
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsItem

THAIGER_FEED_URL = "https://thethaiger.com/feed"

def clean_thaiger_description(raw_html):
    """
    Parses the raw HTML from the description and returns only the text
    from the first <p> tag. This excludes any subsequent paragraphs (like
    the one with "The story ..." text).
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    first_p = soup.find("p")
    if first_p:
        return first_p.get_text(strip=True)
    return raw_html.strip()

class Command(BaseCommand):
    help = "Scrapes The Thaiger RSS feed, extracts publisher and article images, and cleans the description."

    def handle(self, *args, **options):
        self.stdout.write(f"Fetching Thaiger feed from: {THAIGER_FEED_URL}")
        feed = feedparser.parse(THAIGER_FEED_URL)

        if feed.bozo:
            self.stderr.write("Error parsing The Thaiger feed. Please check the URL or feed structure.")
            return

        # Extract top-level publisher info from <image> tag
        publisher_name = None
        publisher_logo_url = None

        if hasattr(feed.feed, "title"):
            publisher_name = feed.feed.title  # e.g. "Thaiger"
        if hasattr(feed.feed, "image") and feed.feed.image:
            if hasattr(feed.feed.image, "title"):
                publisher_name = feed.feed.image.title or publisher_name
            if hasattr(feed.feed.image, "url"):
                publisher_logo_url = feed.feed.image.url

        entries = feed.entries
        self.stdout.write(f"Found {len(entries)} entries in The Thaiger RSS feed.")

        for entry in entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            raw_description = entry.get("description", "").strip()

            # Clean the description: extract only the first <p> tag
            description = clean_thaiger_description(raw_description)

            # Convert published date
            published_parsed = entry.get("published_parsed")
            if published_parsed:
                pub_date = datetime.fromtimestamp(time.mktime(published_parsed))
            else:
                pub_date = datetime.now()

            # Extract article image URL from content:encoded if available
            image_url = None
            raw_html = None
            if "content:encoded" in entry:
                raw_html = entry["content:encoded"]
            elif "content" in entry and isinstance(entry["content"], list):
                raw_html = entry["content"][0].get("value", "")
            if raw_html:
                soup = BeautifulSoup(raw_html, "html.parser")
                first_img = soup.find("img")
                if first_img and first_img.get("src"):
                    image_url = first_img["src"]

            # Check for duplicates by source_link
            if NewsItem.objects.filter(source_link=link).exists():
                self.stdout.write(f"Skipping existing article: {title}")
                continue

            # Create and save the NewsItem
            news_item = NewsItem(
                title=title,
                summary=description,
                source_link=link,
                image_url=image_url,
                publisher_name=publisher_name,
                publisher_logo_url=publisher_logo_url,
                date_published=pub_date,
            )
            news_item.save()
            self.stdout.write(f"Saved new Thaiger article: {title}")

        self.stdout.write("Thaiger RSS scraping complete.")
