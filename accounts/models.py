from django.db import models
from django.contrib.auth.models import AbstractUser
from etc.choices import USER_ROLES, GENDER_CHOICES


class CustomUser(AbstractUser):
    role = models.CharField(max_length=14, choices=USER_ROLES, default='patient')
    phone_number = models.CharField(max_length=13, blank=False, null=False)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False, null=False)

    def __str__(self):
        return f"{self.username} - {self.role}"

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'

    def is_admin(self):
        return self.role == 'admin'

    def is_receptionist(self):
        return self.role == 'receptionist'
