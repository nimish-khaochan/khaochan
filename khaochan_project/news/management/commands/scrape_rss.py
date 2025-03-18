import feedparser
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from news.models import NewsItem

RSS_FEED_URLS = [
    "https://www.bangkokpost.com/rss/data/most-recent.xml",
    "https://www.bangkokpost.com/rss/data/topstories.xml",
    "https://www.bangkokpost.com/rss/data/thailand.xml",
    "https://www.bangkokpost.com/rss/data/business.xml",
    "https://www.bangkokpost.com/rss/data/property.xml",
]

class Command(BaseCommand):
    help = "Scrapes Bangkok Post RSS feeds and inserts new articles into the database."

    def handle(self, *args, **kwargs):
        for feed_url in RSS_FEED_URLS:
            self.stdout.write(f"Processing feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                description = entry.get("description", "").strip()
                published_parsed = entry.get("published_parsed")

                if published_parsed:
                    pub_date = datetime.fromtimestamp(time.mktime(published_parsed))
                else:
                    pub_date = datetime.now()

                # Check for duplicates based on source_link
                if NewsItem.objects.filter(source_link=link).exists():
                    self.stdout.write(f"Article already exists: {title}")
                    continue

                # Create a new NewsItem; note: we ignore image data for now.
                news_item = NewsItem(
                    title=title,
                    summary=description,
                    source_link=link,
                    date_published=pub_date,
                )
                news_item.save()
                self.stdout.write(f"Saved article: {title}")
        self.stdout.write("RSS feed scraping complete.")
