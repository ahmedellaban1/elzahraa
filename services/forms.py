from django import forms
from .models import Service, ServiceRecord
from patients.models import Patient
from staff.models import Doctor

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['patient', 'service', 'doctor', 'doctor_money', 'clinic_money']
        widgets = {
            'doctor_money': forms.NumberInput(attrs={'class': 'form-control', 'id': 'doctorMoneyInput', 'step': '0.01'}),
            'clinic_money': forms.NumberInput(attrs={'class': 'form-control', 'id': 'clinicMoneyInput', 'step': '0.01', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['patient'].queryset = Patient.objects.filter(pk=self.instance.patient_id)
            self.fields['doctor'].queryset = Doctor.objects.filter(pk=self.instance.doctor_id)
            self.fields['service'].queryset = Service.objects.filter(pk=self.instance.service_id)
        else:
            self.fields['patient'].queryset = Patient.objects.none()
            self.fields['doctor'].queryset = Doctor.objects.none()
            self.fields['service'].queryset = Service.objects.none()

        self.fields['patient'].widget.attrs.update({'id': 'patientSelect'})
        self.fields['doctor'].widget.attrs.update({'id': 'doctorSelect'})
        self.fields['service'].widget.attrs.update({'id': 'serviceSelect'})
