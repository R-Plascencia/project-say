from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        if request.POST['userpass'] == request.POST['userpass2']:
            try:
                user = User.objects.get(username=request.POST['email'])
                return render(request, 'accounts/register.html', {'error': 'The email you entered is already taken.'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['email'], password=request.POST['userpass'])
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/register.html', {'error': 'Passwords did not match.'})
    else:
        return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['userpass']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                if request.POST['next'] is not None:
                    return redirect(request.POST['next'])
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Login information is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
