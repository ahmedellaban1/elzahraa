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
    session_number = models.PositiveIntegerField(null=True, blank=True, editable=False) # Daily queue number
    room_number = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='confirmed')
    cost = models.FloatField(null=False, blank=False)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='appointments_created')
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='appointments_updated', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.session_number:
            from datetime import datetime, time
            # Get start and end of the appointment date
            day_start = datetime.combine(self.date.date(), time.min)
            day_end = datetime.combine(self.date.date(), time.max)
            
            # Find the last appointment for this doctor on this specific day
            last_appointment = Appointment.objects.filter(
                doctor=self.doctor,
                date__range=(day_start, day_end)
            ).order_by('-session_number').first()
            
            if last_appointment and last_appointment.session_number:
                self.session_number = last_appointment.session_number + 1
            else:
                self.session_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.session_number} - {self.patient} || {self.doctor} || {self.date.date()}'

        
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
    