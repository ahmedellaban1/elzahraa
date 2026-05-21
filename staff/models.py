from django.db import models
from etc.choices import EXAMINATION_TYPE_CHOICES
from django.core.exceptions import ValidationError


class Doctor(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='doctor')
    specialization = models.CharField(max_length=100, blank=True, null=True)
    examination_type = models.CharField(max_length=10, choices=EXAMINATION_TYPE_CHOICES, null=True, blank=True)
    percentage_value = models.FloatField(null=True, blank=True)
    price_value = models.FloatField(null=True, blank=True) # if it time_share it is just amount of money not percentage.

    def clean(self):
        if not self.price_value and not self.percentage_value:
            raise ValidationError('You must enter either the percentage value or the price value')

    def is_percentage_type(self):
        return self.examination_type == EXAMINATION_TYPE_CHOICES[0][0]

    def is_time_share_type(self):
        return self.examination_type == EXAMINATION_TYPE_CHOICES[1][0]

    def __str__(self):
        return f"{self.user.get_full_name()}"
    

class Receptionist(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='receptionist')
    salary = models.FloatField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.get_full_name()}"
