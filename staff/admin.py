from django.contrib import admin
from .models import Doctor, Receptionist


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'examination_type', 'percentage_value')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('examination_type',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Doctor Name'


@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'salary', 'hire_date')
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('hire_date',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Receptionist Name'
