from django.shortcuts import render
from .models import NewsItem

def home(request):
    # Fetch the latest 12 news items by date
    news_items = NewsItem.objects.order_by('-date_published')[:12]
    return render(request, 'home.html', {'news_items': news_items})


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
            # Log the user in after successful registration
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})