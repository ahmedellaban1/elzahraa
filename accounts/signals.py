from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from patients.models import Patient
from staff.models import Doctor, Receptionist

from django.contrib.auth.models import Group

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create Profile
        if instance.role == 'patient':
            Patient.objects.get_or_create(user=instance)
        elif instance.role == 'doctor':
            Doctor.objects.get_or_create(user=instance)
        elif instance.role == 'receptionist':
            Receptionist.objects.get_or_create(user=instance)
            
        # Assign Group
        group_map = {
            'patient': 'patient_permissions',
            'doctor': 'doctor_permissions',
            'receptionist': 'receptionist_permissions',
            'admin': 'admin_permissions',
        }
        
        group_name = group_map.get(instance.role)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
