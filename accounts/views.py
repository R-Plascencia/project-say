from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        if request.POST['userpass'] == request.POST['userpass2']:
            try:
                user = User.objects.get(username=request.POST['uEmail'])
                return render(request, 'welcome.html', {'reg_error': 'The email you entered is already taken. Please choose a new one.'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['uEmail'], first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['uEmail'], password=request.POST['userpass'])
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'welcome.html', {'reg_error': 'The passwords entered did not match.'})
    else:
        return render(request, 'welcome.html')

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
            return redirect('index')
        else:
            return render(request, 'welcome.html', {'login_error': 'Login information is incorrect.'})
    else:
        return render(request, 'welcome.html')

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
