from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.list_medicines, name='list_medicines'),
    path('add/', views.add_medicine, name='add_medicine'),
    path('<int:pk>/edit/', views.edit_medicine, name='edit_medicine'),
    path('<int:pk>/toggle/', views.toggle_medicine, name='toggle_medicine'),
    path('search/', views.search_medicines, name='search_medicines'),
]
