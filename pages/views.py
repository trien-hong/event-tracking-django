from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import views
from . models import UserEvents
from . import forms
import ticketmaster_api

def login_page(request):
    if request.method == "GET":
        login_form = forms.Login()
        return render(request, 'login_page.html', { 'login_form': login_form })
    if request.method == "POST":
        user_info = request.POST
        form = forms.Login(user_info)
        if form.is_valid():
            user = authenticate(request, username=user_info["username"], password=user_info["password"])
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Login successful!")
                return redirect(index)
            else:
                messages.add_message(request, messages.ERROR, "The username and/or password seem to be incorrect. Please try again.")
                return redirect(login_page)
        else:
            messages.add_message(request, messages.ERROR, "The username and/or password seem to be incorrect. Please try again.")
            return redirect(login_page)

def signup_page(request):
    if request.method == "GET":
        signup_form = forms.Signup()
        return render(request, 'signup_page.html', { 'signup_form': signup_form })
    if request.method == "POST":
        user_info = request.POST
        form = forms.Signup(user_info)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data["username"], password=form.cleaned_data["password"], zip_code=form.cleaned_data["zip_code"])
            messages.add_message(request, messages.SUCCESS, "User has been successfully created. You may now login.")
            return redirect(signup_page)
        else:
            errors = list(form.errors.values())
            error_string = "ERROR(S):<br>"
            for i in range(len(errors)):
                error_string = error_string + str(list(form.errors.values())[i][0]) + "<br>"
            messages.add_message(request, messages.ERROR, mark_safe(error_string))
            return redirect(signup_page)

def password_reset(request):
    if request.method == "GET":
        return render(request, 'password_reset.html')
    if request.method == "POST":
        user_info = request.POST
        if User.objects.filter(username=user_info["username"]).exists():
            if user_info["new_password"] == user_info["confirm_new_password"]:
                reset_password = User.objects.get(username=user_info["username"])
                reset_password.set_password(user_info["new_password"])
                reset_password.save()
                messages.add_message(request, messages.SUCCESS, "The password associated with the username has been reset. You can now login.")
                return redirect(password_reset)
            else:
                messages.add_message(request, messages.ERROR, "Passwords do not match. Please ensure both password fields match.")
                return redirect(password_reset)
        else:
            messages.add_message(request, messages.ERROR, "The username does not exist.")
            return redirect(password_reset)

@login_required
def index(request):
    events = ticketmaster_api.getEvents(str(request.user.zip_code))
    if events == False:
        messages.add_message(request, messages.INFO, "The ZIP code on your profile does not contain any events.")
    return render(request, 'index.html', { "events": events })

@login_required
def search(request):
    if request.method == "GET":
        return render(request, 'search.html', { "events": request.session["events"], "input": request.session["input"]})
    if request.method == "POST":
        input = request.POST
        events = ticketmaster_api.getEvents(str(input["user_input"]))
        request.session["events"] = list(events)
        request.session["input"] = input["user_input"]
        return redirect(search)

@login_required
def profile(request):
    if UserEvents.objects.filter(user_id=request.user.id).exists():
        events = list(UserEvents.objects.all().filter(user_id=request.user.id))
        return render(request, 'profile.html', { "username": request.user.username, "events": events })
    else:
        messages.add_message(request, messages.INFO, "You currently do not have any events in your list.")
        return render(request, 'profile.html', { "username": request.user.username })

@login_required
def settings(request):
    if request.method == "GET":
        return render(request, 'settings.html', { "username": request.user.username })
    if request.method == "POST":
        user_info = request.POST
        # it doesn't go through all the checks for a typical username/password
        # mostly just basic checks there are a few edge cases I believe
        if user_info["new_username"] != "" and user_info["new_username"].isspace() == False:
            if User.objects.filter(username=user_info["new_username"]).exists():
                messages.add_message(request, messages.ERROR, "The username already exist.")
                return redirect(settings)
            else:
                update_username = User.objects.get(id=request.user.id)
                update_username.username = user_info["new_username"]
                update_username.save()
        if user_info["new_zip_code"] != "":
            if user_info["new_zip_code"].isnumeric():
                update_zip_code = User.objects.get(id=request.user.id)
                update_zip_code.zip_code = user_info["new_zip_code"]
                update_zip_code.save()
            else:
                messages.add_message(request, messages.ERROR, "ZIP Code should only contain numeric values (0-9).")
                return redirect(settings)
        if user_info["new_password"] != "" and user_info["confirm_new_password"] != "":
            if user_info["new_password"] == user_info["confirm_new_password"]:
                update_password = User.objects.get(id=request.user.id)
                update_password.set_password(user_info["new_password"])
                update_password.save()
                messages.add_message(request, messages.SUCCESS, "All applicable fields have been updatded. Please login again.")
                return redirect(login_page)
            else:
                messages.add_message(request, messages.ERROR, "Passwords do not match. Please ensure both password fields match.")
                return redirect(settings)
        if user_info["new_username"] == "" and user_info["new_password"] == "" and user_info["confirm_new_password"] == "" and user_info["new_zip_code"] == "":
            messages.add_message(request, messages.ERROR, "The fields seem to be empty.")
            return redirect(settings)
        else:
            messages.add_message(request, messages.SUCCESS, "All applicable fields have been updatded.")
            return redirect(settings)

@login_required
def addEventToDatabase(request):
    if request.method == "POST":
        event_info = request.POST
        if UserEvents.objects.filter(user_id=request.user.id, event_id=event_info["eventId"]).exists():
            messages.add_message(request, messages.ERROR, "You already have this event in your list. Try adding a different event.")
        else:
            add_event = UserEvents(event_id=event_info["eventId"], event_title=event_info["eventTitle"], event_image_url=event_info["eventImageUrl"], event_date=event_info["eventDate"], event_location=event_info["eventLocation"], event_price=event_info["eventPrice"], user_id=request.user.id)
            add_event.save()
            messages.add_message(request, messages.SUCCESS, "Event was successfully added to your list.")
    if event_info["locationOfUrl"] == "search":
        return redirect(search)
    else:
        return redirect(index)

@login_required
def deleteEventFromDatabase(request):
    if request.method == "POST":
        event_info = request.POST
        delete_event = UserEvents.objects.get(event_id=event_info["eventId"], user_id=request.user.id)
        delete_event.delete()
        if UserEvents.objects.filter(user_id=request.user.id).exists():
            messages.add_message(request, messages.SUCCESS, "Event was successfully deleted from your list.")
    return redirect(profile)

@login_required
def logout_action(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successful!")
    return redirect(login_page)