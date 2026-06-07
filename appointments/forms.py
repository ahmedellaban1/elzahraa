from django import forms
from .models import Appointment
from patients.models import Patient
from staff.models import Doctor

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'room_number', 'status', 'cost', 'doctor_money', 'clinic_money', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'room_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'id': 'costInput', 'step': '0.01'}),
            'doctor_money': forms.NumberInput(attrs={'class': 'form-control', 'id': 'doctorMoneyInput', 'step': '0.01'}),
            'clinic_money': forms.NumberInput(attrs={'class': 'form-control', 'id': 'clinicMoneyInput', 'step': '0.01', 'readonly': 'readonly'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We need the current choices to be present so Tom Select displays them on load
        if self.instance and self.instance.pk:
            self.fields['patient'].queryset = Patient.objects.filter(pk=self.instance.patient_id)
            self.fields['doctor'].queryset = Doctor.objects.filter(pk=self.instance.doctor_id)
        else:
            self.fields['patient'].queryset = Patient.objects.none()
            self.fields['doctor'].queryset = Doctor.objects.none()
            
        self.fields['patient'].widget.attrs.update({'id': 'patientSelect'})
        self.fields['doctor'].widget.attrs.update({'id': 'doctorSelect'})
