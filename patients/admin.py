from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone_number', 'birth_date', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number', 'address')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Patient Name'

    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.short_description = 'Phone Number'
