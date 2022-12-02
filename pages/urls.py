from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.settings, name='settings'),
    path('addEventToDatabase/', views.addEventToDatabase, name='addEventToDatabase'),
    path('deleteEventFromDatabase/', views.deleteEventFromDatabase, name='deleteEventFromDatabase'),
    path('event_details/', views.event_details, name='event_details'),
    path('logout_action/', views.logout_action, name='logout_action'),
]