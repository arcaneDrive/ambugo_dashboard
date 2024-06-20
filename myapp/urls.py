from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index ,name='index'),

    path('input-data/', views.booking_page, name='booking_page'),  # URL for Input Data (Booking Page)
    path('retrieve-data/', views.booking_history, name='booking_history'),  # URL for Retrieve Data (Booking History)
    path('confirmation/', views.confirmation_page, name='confirmation_page'),  # URL for Confirmation Page
    path('registration/', views.ambulance_registration, name='ambulance_registration'),  # URL for Confirmation Page
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]

