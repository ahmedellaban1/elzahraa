from django.contrib import admin
from .models import Service, ServiceRecord


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'clinic_percentage', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service', 'doctor', 'doctor_amount', 'clinic_amount', 'created_at')
    list_filter = ('service', 'doctor', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'service__name', 'doctor__user__first_name')
    readonly_fields = ('doctor_amount', 'clinic_amount', 'created_at', 'updated_at')
