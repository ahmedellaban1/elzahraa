from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('add-service/<int:patient_id>/', views.add_service, name='add_service_for_patient'),
    path('define-service/', views.create_service, name='define_service'),
    path('', views.service_list, name='list'),
    path('<int:pk>/', views.service_detail, name='detail'),
]
