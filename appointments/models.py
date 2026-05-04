from django.db import models
from etc.choices import (
    APPOINTMENT_STATUS_CHOICES, MEDICINE_DOSAGE_UNIT_CHOICES,
    MEDICINE_FREQUENCY_CHOICES, MEDICINE_DURATION_UNIT_CHOICES, 
    MEDICINE_ROUTE_CHOICES, MEDICINE_NOTES
)


class Appointment(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('staff.Doctor', on_delete=models.CASCADE, related_name='appointments')
    date = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='confirmed')
    cost = models.FloatField(null=False, blank=False)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='appointments_created')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='appointments_updated', null=True, blank=True)

    def __str__(self):
        return f'{self.patient} || {self.doctor} || {self.date}'

        
class PrescriptionItem(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescription_items')
    medicine = models.ForeignKey('medicines.Medicine', on_delete=models.CASCADE, related_name='prescription_items')
    dosage = models.IntegerField(null=False, blank=False)
    dosage_unit = models.CharField(max_length=20, choices=MEDICINE_DOSAGE_UNIT_CHOICES, null=False, blank=False)
    frequency = models.CharField(max_length=20, choices=MEDICINE_FREQUENCY_CHOICES, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)
    duration_unit = models.CharField(max_length=20, choices=MEDICINE_DURATION_UNIT_CHOICES, null=False, blank=False)
    route = models.CharField(max_length=20, choices=MEDICINE_ROUTE_CHOICES, null=False, blank=False)
    notes = models.CharField(max_length=25, choices=MEDICINE_NOTES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='prescription_items_created')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='prescription_items_updated', null=True, blank=True)

    def __str__(self):
        return f'{self.medicine} || {self.appointment}'
    