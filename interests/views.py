from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Interest
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.template.defaulttags import register
from newsitems.utils import build_results
import feedparser
import re

# Dictionary of all allowed RSS sources of news
# rss_sources = {'AP': 'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa',
#     'Reuters - Politics': 'http://feeds.reuters.com/Reuters/PoliticsNews',
#     'Reuters - Domestic': 'http://feeds.reuters.com/Reuters/domesticNews',
#     'The Economist - United States': 'http://www.economist.com/sections/united-states/rss.xml',
#     'The Economist - Economics': 'http://www.economist.com/sections/economics/rss.xml',
#     'Financial Times - US': 'http://www.ft.com/rss/world/us',
#     'Financial Times - US&CAN Politics': 'http://www.ft.com/rss/world/us/politics',
#     'The Independent': 'http://www.independent.co.uk/news/world/americas/rss',
#     'BBC': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml'
# }

# Create your views here.
@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['keywords']:
            interest = Interest()
            interest.title = request.POST['title']
            interest.keywords = request.POST['keywords']
            interest.pub_date = timezone.now()
            interest.creator = request.user
            interest.save()
            request.user.profile.interests.add(interest)
            results = build_results(request, interest)
            return redirect('home')
        else:
            return render(request, 'interests/create.html', {'error':'ERROR: Interest must have a title and maximum of 4 keywords'})
    else:
        print("WHY ARE WE HERE")
        return render(request, 'interests/create.html')

def home(request):
    if request.user.is_anonymous():
        return render(request, 'interests/home.html')
    else:
        interests = request.user.profile.interests
        return render(request, 'interests/home.html', {'interests': interests})

def list(request):
    interests = Interest.objects.order_by('title')
    return render(request, 'interests/list.html', {'interests':interests})

def copy(request, pk):
    if request.method == 'POST':
        interest = Interest.objects.get(pk=pk)
        interest.num_of_imports += 1
        interest.save()
        u = request.user
        u.profile.interests.add(interest)
        u.profile.save()
        return redirect('home')
