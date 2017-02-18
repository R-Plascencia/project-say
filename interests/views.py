from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Interest
from django.contrib.auth.models import User
from accounts.models import UserProfile

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
            return redirect('home')
        else:
            return render(request, 'interests/create.html', {'error':'ERROR: Interest must have a title and maximum of 4 keywords'})
    else:
        return render(request, 'interests/create.html')

def home(request):
    interests = Interest.objects.order_by('pub_date')
    return render(request, 'interests/home.html', {'interests':interests})

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
