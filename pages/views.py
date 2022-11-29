from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
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
            messages.add_message(request, messages.ERROR, "The username and/or password seem to be incorrect. Please try again.")
            return redirect(login_page)

def signup_page(request):
    if request.method == "GET":
        return render(request, 'signup_page.html')
    if request.method == "POST":
        user_info = request.POST
        if User.objects.filter(username=user_info["username"]).exists():
            messages.add_message(request, messages.ERROR, "Username already exist. Try a different username or try logging in.")
            return redirect(signup_page)
        elif user_info["password"] != user_info["confirm_password"]:
            messages.add_message(request, messages.ERROR, "Passwords do not match. Please ensure both password fields match.")
            return redirect(signup_page)
        elif user_info["zip"].isnumeric() is False:
            messages.add_message(request, messages.ERROR, "ZIP Code should only contain numeric values (0-9).")
            return redirect(signup_page)
        else:
            user = User.objects.create_user(username=user_info["username"], password=user_info["password"], zip=user_info["zip"])
            return redirect(login_page)

@login_required
def index(request):
    return render(request, 'index.html', { "username": request.user.username, "password": request.user.password, "zip": request.user.zip })

@login_required
def logout_action(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successful!")
    return redirect(login_page)