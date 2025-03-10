from django.contrib import admin
from .models import NewsItem

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published')
    search_fields = ('title', 'summary')