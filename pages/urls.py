from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('index/', views.index, name='index'),
    path('index/addEventToDatabase/', views.addEventToDatabase, name='addEventToDatabase'),
    path('profile/', views.profile, name='profile'),
    path('profile/deleteEventFromDatabase/', views.deleteEventFromDatabase, name='deleteEventFromDatabase'),
    path('profile/settings', views.settings, name='settings'),
    path('logout_action/', views.logout_action, name='logout_action'),
]