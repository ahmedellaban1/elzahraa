from django import forms
from django.contrib.auth import get_user_model
from .models import Patient
from etc.choices import GENDER_CHOICES

User = get_user_model()

class PatientCreationForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=150, label="الاسم الأول", required=True)
    last_name = forms.CharField(max_length=150, label="اسم العائلة", required=True)
    username = forms.CharField(max_length=150, label="اسم المستخدم", required=True, help_text="يمكن استخدام رقم الهاتف كاسم مستخدم")
    phone_number = forms.CharField(max_length=13, label="رقم الهاتف", required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="الجنس", required=True)
    
    # Patient fields
    address = forms.CharField(max_length=100, label="العنوان", required=False)
    birth_date = forms.DateField(label="تاريخ الميلاد", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    notes = forms.CharField(label="ملاحظات", required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add special classes for premium look
        self.fields['gender'].widget.attrs.update({'class': 'form-select'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        if commit:
            user.save()
            # Create or update the patient profile
            Patient.objects.update_or_create(
                user=user,
                defaults={
                    'address': self.cleaned_data.get('address'),
                    'birth_date': self.cleaned_data.get('birth_date'),
                    'notes': self.cleaned_data.get('notes'),
                }
            )
        return user
