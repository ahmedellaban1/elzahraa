from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from patients.models import Patient
from staff.models import Doctor, Receptionist

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'patient':
            Patient.objects.get_or_create(user=instance)
        elif instance.role == 'doctor':
            Doctor.objects.get_or_create(user=instance)
        elif instance.role == 'receptionist':
            Receptionist.objects.get_or_create(user=instance)
