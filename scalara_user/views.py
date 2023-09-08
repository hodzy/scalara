from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import LoginForm


def create_users():
    user = User.objects.create_user(username="Alex", password="pass")
    user.save()

    user = User.objects.create_user(username="Basti", password="pass")
    user.save()

    user = User.objects.create_user(username="Hady", password="pass")
    user.save()

# Create your views here.
def login_user(request):
    # check if user is already logged in
    # user_name = request.session.get('user', None)
    # if user_name:
    #     return HttpResponse(f'you are logged in as {user_name}')

    # check if userbase is already created
    if not User.objects.filter(username='Alex').exists():
        create_users()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_authenticated = authenticate(username=username, password=password)
            print(user_authenticated)
            print(username)
            print(password)
            if user_authenticated:
                request.session['user'] = username
                return redirect('upload')
            else:
                print('false cerdentials')
    else:
        if not request.session.get('user', None):
            request.session['user'] = None
        form = LoginForm()
    return render(request, "login.html",{"form": form, "username": request.session['user']})

def logout_user(request):
    request.session['user'] = None
    return redirect('login')