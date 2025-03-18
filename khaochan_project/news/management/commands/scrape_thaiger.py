import feedparser
import time
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsItem

THAIGER_FEED_URL = "https://thethaiger.com/feed"

def clean_thaiger_description(raw_html):
    """
    1. Parse the raw HTML with BeautifulSoup.
    2. Extract the FIRST <p> tag's text only.
    3. Truncate the text after encountering two full stops ('.').
    4. Return plain text with no HTML tags.
    """
    soup = BeautifulSoup(raw_html, "html.parser")

    # 1. Find the first <p> tag
    first_p = soup.find('p')
    if first_p:
        text = first_p.get_text(strip=True)
    else:
        # fallback if there's no <p> tag, use all text
        text = soup.get_text(strip=True)

    # 2. Truncate after two periods
    text = truncate_after_two_periods(text)

    return text.strip()

def truncate_after_two_periods(text):
    """
    Finds the first two '.' (periods) in the text.
    Returns everything up to (and including) the second period.
    If fewer than two periods are found, return the entire text.
    """
    first_dot = text.find('.')
    if first_dot == -1:
        return text  # no periods at all, return entire text

    second_dot = text.find('.', first_dot + 1)
    if second_dot == -1:
        return text  # only one period found, return entire text

    # Return substring up to and including the second period
    return text[:second_dot + 1]

class Command(BaseCommand):
    help = "Scrapes Thaiger RSS feed, cleans the description, and inserts new articles into the DB."

    def handle(self, *args, **options):
        self.stdout.write(f"Fetching feed from: {THAIGER_FEED_URL}")
        feed = feedparser.parse(THAIGER_FEED_URL)

        if feed.bozo:
            self.stderr.write("Error parsing the feed. Please check the URL or feed structure.")
            return

        entries = feed.entries
        self.stdout.write(f"Found {len(entries)} entries in Thaiger RSS feed.")

        for entry in entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()

            # Grab the raw HTML from the <description> element
            raw_description = entry.get("description", "")
            # Clean + truncate it
            description = clean_thaiger_description(raw_description)

            # Convert the published date to datetime
            published_parsed = entry.get("published_parsed")
            if published_parsed:
                pub_date = datetime.fromtimestamp(time.mktime(published_parsed))
            else:
                pub_date = datetime.now()

            # Check for duplicates by link
            if NewsItem.objects.filter(source_link=link).exists():
                self.stdout.write(f"Skipping existing article: {title}")
                continue

            # Create a new NewsItem; ignoring images for now
            news_item = NewsItem(
                title=title,
                summary=description,
                source_link=link,
                date_published=pub_date,
            )
            news_item.save()
            self.stdout.write(f"Saved new article: {title}")

        self.stdout.write("Thaiger RSS scraping complete.")
