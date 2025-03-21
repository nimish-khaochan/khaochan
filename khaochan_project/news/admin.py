from django.contrib import admin
from .models import NewsItem

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_top_news", "date_published")
    list_filter = ("category", "is_top_news")
    search_fields = ("title", "summary")
