from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('get-doctor/', views.get_doctor, name='get_doctor'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
