from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('get-doctor/', views.get_doctor, name='get_doctor'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create-doctor/', views.create_doctor, name='create_doctor'),
    path('create-receptionist/', views.create_receptionist, name='create_receptionist'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctor/<int:pk>/export-excel/', views.export_doctor_excel, name='export_doctor_excel'),
    path('doctor/<int:pk>/reset-password/', views.reset_doctor_password, name='reset_doctor_password'),
]
