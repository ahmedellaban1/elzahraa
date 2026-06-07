from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('add-service/<int:patient_id>/', views.add_service, name='add_service_for_patient'),
    path('add-service/', views.add_service, name='add_service'),
    path('define-service/', views.create_service, name='define_service'),
    path('get-services/', views.get_services_json, name='get_services'),
    path('', views.service_list, name='list'),
    path('<int:pk>/', views.service_detail, name='detail'),
    path('<int:pk>/edit/', views.update_service, name='update_service'),
    path('<int:pk>/delete/', views.delete_service, name='delete_service'),
    path('record/<int:pk>/edit/', views.update_service_record, name='update_service_record'),
    path('record/<int:pk>/delete/', views.delete_service_record, name='delete_service_record'),
]
