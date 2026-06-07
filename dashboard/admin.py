from django.contrib import admin
from .models import DiscountRecord, Expense


@admin.register(DiscountRecord)
class DiscountRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'discount_type', 'patient', 'original_amount', 'discount_amount', 'final_amount', 'created_by')
    list_filter = ('discount_type', 'date')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'reason')
    readonly_fields = ('created_at', 'final_amount')
    date_hierarchy = 'date'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'description', 'amount', 'created_by')
    list_filter = ('category', 'date')
    search_fields = ('description', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
