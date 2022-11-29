from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import views

def login_page(request):
    if request.method == "GET":
        return render(request, 'login_page.html')
    if request.method == "POST":
        user_info = request.POST
        user = authenticate(request, username=user_info["username"], password=user_info["password"])
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.add_message(request, messages.INFO, "The username and/or password seem to be incorect. Please try again.")
            return redirect(login_page)

def signup_page(request):
    if request.method == "GET":
        return render(request, 'signup_page.html')
    if request.method == "POST":
        user_info = request.POST
        if User.objects.filter(username=user_info["username"]).exists():
            messages.add_message(request, messages.INFO, "Username already exist. Try a different username or try logging in.")
            return redirect(signup_page)
        else:
            user = User.objects.create_user(username=user_info["username"], password=user_info["password"])
            return redirect(login_page)

@login_required
def index(request):
    return render(request, 'index.html', { "username": request.user.username })

@login_required
def logout_action(request):
    logout(request)
    return redirect(login_page)