from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('add/', views.add_medicine, name='add_medicine'),
]
