from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'scientific_name', 'concentration', 'concentration_unit', 'is_active')
    list_filter = ('is_active', 'concentration_unit')
    search_fields = ('trade_name', 'scientific_name')
    readonly_fields = ('created_at',)
