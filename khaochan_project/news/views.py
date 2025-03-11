from django.shortcuts import render
from .models import NewsItem

def home(request):
    # Fetch the latest 12 news items by date
    news_items = NewsItem.objects.order_by('-date_published')[:12]
    return render(request, 'home.html', {'news_items': news_items})
