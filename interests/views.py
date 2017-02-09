from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Interest
from django.contrib.auth.models import User

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
            return redirect('home')
        else:
            return render(request, 'interests/create.html', {'error':'ERROR: Interest must have a title and maximum of 4 keywords'})
    else:
        return render(request, 'interests/create.html')

def home(request):
    interests = Interest.objects.order_by('pub_date')
    return render(request, 'interests/home.html', {'interests':interests})
