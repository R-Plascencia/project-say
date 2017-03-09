from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Interest
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.template.defaulttags import register
from newsitems.utils import build_results
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
            results = build_results(request, interest)
            return redirect('home')
        else:
            return render(request, 'interests/create.html', {'error':'Interest must have a title and maximum of 4 keywords'})
    else:
        return render(request, 'interests/create.html')

def refresh(request, pk):
    if request.method == 'POST':
        # request.user.profile.interests.newsresults.newsitems.all.delete()
        interest = Interest.objects.get(pk=pk)
        NewsResult.objects.filter(interest__id=pk).delete()
        results = build_results(request, interest)
        return redirect('home')

def home(request):
    if request.user.is_anonymous():
        return render(request, 'interests/home.html')
    else:
        interests = request.user.profile.interests
        return render(request, 'interests/home.html', {'interests': interests})

def search(request):
    search_query = request.GET.get('searchtitle')
    search_result = Interest.objects.filter(title__contains=search_query).order_by('num_of_imports')
    return render(request, 'interests/list.html', {'search_result':search_result, 'searchtitle':search_query, 'order_by': 'num_of_imports'})

def list(request):
    order_by = request.GET.get('order_by', 'num_of_imports')
    first_time = False
    if request.GET.get('sort'):
        sort_type = request.GET.get('sort')
    else:
        first_time = True
        sort_type = 'ascending'

    if sort_type == 'ascending':
        interests = Interest.objects.order_by('-' + order_by)
        if not first_time: sort_type = 'descending'
    else:
        interests = Interest.objects.order_by(order_by)
        sort_type = 'ascending'
    return render(request, 'interests/list.html', {'interests':interests, 'sort_type':sort_type, 'order_by':order_by})

def copy(request, pk):
    if request.method == 'POST':
        interest = Interest.objects.get(pk=pk)
        interest.num_of_imports += 1
        interest.save()
        u = request.user
        u.profile.interests.add(interest)
        u.profile.save()
        return redirect('home')

def remove(request, pk):
    if request.method == 'POST':
        interest = Interest.objects.get(pk=pk)
        request.user.profile.interests.remove(interest)
        interest.delete()
        return render(request, 'interests/home.html')
