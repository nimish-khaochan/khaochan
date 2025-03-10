from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=200, help_text="Headline of the news item.")
    summary = models.TextField(help_text="A short summary (around 30 words) for quick reading.")
    source_link = models.URLField(help_text="URL linking to the original article.")
    date_published = models.DateTimeField(auto_now_add=True, help_text="Date and time when this news item was created.")

    def __str__(self):
        return self.title
