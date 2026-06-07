from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_appointments, name='list'),
    path('create/', views.create_appointment, name='create'),
    path('update-status/<int:pk>/', views.update_appointment_status, name='update_status'),
    path('update/<int:pk>/', views.update_appointment, name='update'),
    path('prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    path('prescription/<int:appointment_id>/print/', views.print_prescription, name='print_prescription'),
    path('prescription/<int:appointment_id>/save-notes/', views.save_appointment_notes, name='save_notes'),
]
