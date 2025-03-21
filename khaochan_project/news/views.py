from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from .models import NewsItem


def home(request):
    # Fetch all news items, newest first
    all_news = NewsItem.objects.order_by('-date_published')

    # Paginate by 12 items per page
    paginator = Paginator(all_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # If you have top news, you can fetch them here
    top_news = NewsItem.objects.filter(is_top_news=True).order_by('-date_published')[:5]

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'top_news': top_news,
    })


def news_by_category(request, cat):
    """
    Displays news items for a specific category.
    """
    items = NewsItem.objects.filter(category__iexact=cat).order_by('-date_published')
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'selected_category': cat,
    })


def login_view(request):
    return render(request, 'placeholder.html', {'title': 'Login'})


def newsletters_view(request):
    return render(request, 'placeholder.html', {'title': 'Newsletters'})


def about_view(request):
    return render(request, 'placeholder.html', {'title': 'About Us'})


def blog_view(request):
    return render(request, 'placeholder.html', {'title': 'Blog'})


def publishers_view(request):
    return render(request, 'placeholder.html', {'title': 'Publishers'})


def help_view(request):
    return render(request, 'placeholder.html', {'title': 'Help'})


def terms_view(request):
    return render(request, 'placeholder.html', {'title': 'Terms'})


def privacy_view(request):
    return render(request, 'placeholder.html', {'title': 'Privacy Policy'})


def sitemap_view(request):
    return render(request, 'placeholder.html', {'title': 'Sitemap'})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
