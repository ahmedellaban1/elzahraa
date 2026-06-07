from django.contrib import admin
from .models import Appointment, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'status', 'cost', 'doctor_money', 'clinic_money')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'notes')
    inlines = [PrescriptionItemInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'appointment', 'dosage', 'frequency', 'duration')
    list_filter = ('dosage_unit', 'frequency', 'duration_unit', 'route')
    search_fields = ('medicine__trade_name', 'appointment__patient__user__first_name')
