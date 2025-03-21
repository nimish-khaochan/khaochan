from django.db import models

class NewsItem(models.Model):
    class CategoryChoices(models.TextChoices):
        ALERTS = "alerts", "Alerts"
        LOCAL = "local", "Local News"
        CULTURE = "culture", "Culture"
        VISAS = "visas", "Visa Regulations"
        BUSINESS = "business", "Business"

    title = models.CharField(
        max_length=200,
        help_text="Headline of the news item."
    )
    summary = models.TextField(
        help_text="A short summary (around 30 words) for quick reading."
    )
    source_link = models.URLField(
        help_text="URL linking to the original article."
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL of the article image."
    )
    publisher_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of the publisher from the RSS feed."
    )
    publisher_logo_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL of the publisher's logo image from the RSS feed."
    )
    date_published = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this news item was created."
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,  # Dropdown in admin
        blank=True,
        null=True,
        help_text="Select a category for this news item."
    )
    is_top_news = models.BooleanField(
        default=False,
        help_text="Mark if this item is top news."
    )

    def __str__(self):
        return self.title
