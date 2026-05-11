from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('get-patient/', views.get_patient, name='get_patient'),
    path('create-patient/', views.create_patient, name='create_patient'),
    path('<int:pk>/', views.patient_detail, name='detail'),
    path('<int:pk>/reset-password/', views.reset_patient_password, name='reset_password'),
]
