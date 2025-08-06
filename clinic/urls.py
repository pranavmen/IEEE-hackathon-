# CliQ/clinic/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('clinic/<str:pk>/', views.clinic, name="clinic"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-clinic/', views.createClinic, name="create-clinic"),
    path('update-clinic/<str:pk>/', views.updateClinic, name="update-clinic"),
    path('delete-clinic/<str:pk>/', views.deleteClinic, name="delete-clinic"),

    # Dashboards and Booking
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),

    # --- ADD THESE NEW URLS ---
    # Patient URLs
    path('my-appointments/', views.patient_appointments, name='patient_appointments'),
    path('settings/', views.patient_settings, name='patient_settings'),

    # Doctor URLs (You can create separate ones if functionality differs)
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/settings/', views.doctor_settings, name='doctor_settings'),
]