import feedparser
import time
from datetime import datetime
from bs4 import BeautifulSoup
import logging

from django.core.management.base import BaseCommand
from news.models import NewsItem

logger = logging.getLogger(__name__)

RSS_FEED_URLS = [
    "https://www.bangkokpost.com/rss/data/most-recent.xml",
    "https://www.bangkokpost.com/rss/data/topstories.xml",
    "https://www.bangkokpost.com/rss/data/thailand.xml",
    "https://www.bangkokpost.com/rss/data/business.xml",
    "https://www.bangkokpost.com/rss/data/property.xml",
]

class Command(BaseCommand):
    help = "Scrapes Bangkok Post RSS feeds and inserts new articles into the database."

    def handle(self, *args, **options):
        for feed_url in RSS_FEED_URLS:
            self.stdout.write(f"Processing feed: {feed_url}")
            feed = feedparser.parse(feed_url)

            # If there's an error, check if it's solely the encoding warning.
            if feed.bozo:
                exc_message = str(feed.bozo_exception)
                if "document declared as us-ascii" in exc_message and "parsed as utf-8" in exc_message:
                    warning_msg = f"Warning: encoding mismatch in feed {feed_url}. Proceeding with entries."
                    logger.warning(warning_msg)
                    self.stdout.write(warning_msg)
                else:
                    error_msg = f"Error parsing feed: {feed_url}. Exception: {feed.bozo_exception}"
                    logger.error(error_msg)
                    self.stderr.write(error_msg)
                    continue  # Skip this feed if the error is not just an encoding mismatch

            # Extract publisher details from the feed.
            publisher_name = None
            publisher_logo_url = None
            if hasattr(feed.feed, "image") and feed.feed.image:
                if hasattr(feed.feed.image, "title") and feed.feed.image.title:
                    publisher_name = feed.feed.image.title.strip()
                else:
                    publisher_name = feed.feed.title.strip() if hasattr(feed.feed, "title") else "Bangkok Post"

                if hasattr(feed.feed.image, "url") and feed.feed.image.url:
                    publisher_logo_url = feed.feed.image.url.strip()
            else:
                publisher_name = feed.feed.title.strip() if hasattr(feed.feed, "title") else "Bangkok Post"

            entries = feed.entries
            self.stdout.write(f"Found {len(entries)} entries in feed: {feed_url}")

            for entry in entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                description = entry.get("description", "").strip()

                # Parse publication date; if missing, use current time.
                published_parsed = entry.get("published_parsed")
                if published_parsed:
                    pub_date = datetime.fromtimestamp(time.mktime(published_parsed))
                else:
                    pub_date = datetime.now()

                # Attempt to extract an article image URL from the description HTML.
                image_url = None
                soup = BeautifulSoup(description, "html.parser")
                first_img = soup.find("img")
                if first_img and first_img.get("src"):
                    image_url = first_img["src"]

                # Skip duplicate articles based on the source link.
                if NewsItem.objects.filter(source_link=link).exists():
                    self.stdout.write(f"Skipping duplicate article: {title}")
                    continue

                # Create and save a new NewsItem.
                news_item = NewsItem(
                    title=title,
                    summary=description,
                    source_link=link,
                    image_url=image_url,  # This may be None if no image was found.
                    publisher_name=publisher_name,
                    publisher_logo_url=publisher_logo_url,
                    date_published=pub_date,
                )
                try:
                    news_item.save()
                    self.stdout.write(f"Saved article: {title}")
                except Exception as e:
                    save_error = f"Error saving article '{title}': {e}"
                    logger.error(save_error)
                    self.stderr.write(save_error)

        self.stdout.write("Bangkok Post RSS scraping complete.")
