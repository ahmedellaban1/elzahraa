from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_router, name='dashboard_router'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('search/', views.unified_search, name='unified_search'),
]
