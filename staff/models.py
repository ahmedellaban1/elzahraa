from django.db import models
from etc.choices import EXAMINATION_TYPE_CHOICES


class Doctor(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='doctor')
    specialization = models.CharField(max_length=100, blank=True, null=True)
    examination_type = models.CharField(max_length=10, choices=EXAMINATION_TYPE_CHOICES, null=True, blank=True)
    percentage_value = models.FloatField(null=True, blank=True)

    def is_percentage_type(self):
        return self.examination_type == 'percentage'

    def is_time_share_type(self):
        return self.examination_type == 'time_share'

    def __str__(self):
        return f"{self.user.get_full_name()}"
    

class Receptionist(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='receptionist')
    salary = models.FloatField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.get_full_name()}"
