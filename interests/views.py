from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from .models import Interest
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.template.defaulttags import register
from newsitems.utils import populate_newsitems, get_newsitems
from newsitems.models import NewsResult



# Create your views here.
@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['keywords']:
            interest = Interest()
            # Make titles pretty: capitalize first letter of each word
            title = request.POST['title'].split(' ')
            i = 0
            for word in title:
                letter = word[:1].upper()
                new_item = word.replace(word[:1], letter, 1)
                title[i] = new_item
                i += 1
            interest.title = ' '.join(title)
            interest.keywords = request.POST['keywords']
            interest.pub_date = timezone.now()
            interest.last_refreshed = timezone.now()
            interest.creator = request.user
            interest.save()
            request.user.profile.interests.add(interest)
            request.user.profile.save()
            results = get_newsitems(request, interest)
            return redirect('index')
        else:
            return render(request, 'interests/create.html', {'error':'Interest must have a title and maximum of 4 keywords'})
    else:
        return render(request, 'index.html')

def refresh(request, pk):
    if request.method == 'POST':
        interest = Interest.objects.get(pk=pk)
        NewsResult.objects.filter(interest__id=pk).delete()
        results = get_newsitems(request, interest)
        return redirect('index')

def index(request):
    if request.user.is_anonymous():
        return render(request, 'welcome.html')
    else:
        interests = request.user.profile.interests
        return render(request, 'index.html', {'interests': interests, 'profile_id': request.user.profile.id})

def copy(request, pk):
    if request.method == 'POST':
        interest = Interest.objects.get(pk=pk)
        interest.num_of_imports += 1
        interest.save()
        u = request.user
        u.profile.interests.add(interest)
        u.profile.save()
        return redirect('index')

def remove(request, pk):
    if request.method == 'POST':
        interest = Interest.objects.get(pk=pk)
        request.user.profile.interests.remove(interest)
        # interest.delete()
        return redirect('index')

def list(request):
    return render(request, 'index.html')

def buildresults(request):
    populate_newsitems()
    return redirect('index')
