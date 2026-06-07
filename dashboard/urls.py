from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_router, name='dashboard_router'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('search/', views.unified_search, name='unified_search'),
    path('discount/appointment/<int:pk>/', views.add_appointment_discount, name='add_appointment_discount'),
    path('discount/service/<int:pk>/', views.add_service_discount, name='add_service_discount'),
    path('expenses/', views.manage_expenses, name='manage_expenses'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
]
