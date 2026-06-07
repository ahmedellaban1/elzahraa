from django.db import models
from etc.choices import DISCOUNT_TYPE_CHOICES, EXPENSE_CATEGORY_CHOICES

class DiscountRecord(models.Model):
    """Tracks discounts applied to appointments or service records."""
    discount_type = models.CharField(
        max_length=20, choices=DISCOUNT_TYPE_CHOICES,
    )
    # Link to either an appointment or a service record (one is set, the other is null)
    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='discount',
    )
    service_record = models.OneToOneField(
        'services.ServiceRecord',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='discount',
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='discounts',
    )
    original_amount = models.FloatField()
    discount_amount = models.FloatField()
    final_amount = models.FloatField()
    reason = models.TextField(null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='discounts_created',
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        label = self.appointment or self.service_record
        return f'خصم {self.discount_amount} ج.م — {label}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.appointment and not self.service_record:
            raise ValidationError('يجب تحديد موعد أو سجل خدمة.')
        if self.appointment and self.service_record:
            raise ValidationError('لا يمكن ربط الخصم بموعد وخدمة في آنٍ واحد.')


class Expense(models.Model):
    """Tracks clinic operating expenses."""
    category = models.CharField(
        max_length=20, choices=EXPENSE_CATEGORY_CHOICES,
    )
    description = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField()
    notes = models.TextField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='expenses_created',
    )
    updated_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='expenses_updated',
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.get_category_display()} — {self.description} ({self.amount} ج.م) [{self.date}]'
