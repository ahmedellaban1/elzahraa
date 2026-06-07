from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    active = models.BooleanField(default=True)
    price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='services_created')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='services_updated', null=True, blank=True)

    def is_active(self):
        return self.active

    def __str__(self):
        return self.name


class ServiceRecord(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='service_records')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_records')
    doctor = models.ForeignKey('staff.Doctor', on_delete=models.CASCADE, related_name='service_records')
    doctor_money = models.FloatField(null=True, blank=True)
    clinic_money = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='service_records_created')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='service_records_updated', null=True, blank=True)

    def __str__(self):
        return f"{self.service.name} - {self.patient}"