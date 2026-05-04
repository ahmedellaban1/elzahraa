from django.db import models
from etc.choices import CONCENTRATION_UNIT_CHOICES


class Medicine(models.Model):
    trade_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)
    concentration = models.IntegerField(null=True, blank=True)
    concentration_unit = models.CharField(max_length=20, choices=CONCENTRATION_UNIT_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='medicines_created')
    
    def __str__(self):
        return self.trade_name
