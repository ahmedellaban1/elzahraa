from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor, Receptionist
from etc.choices import GENDER_CHOICES, EXAMINATION_TYPE_CHOICES

User = get_user_model()

class DoctorCreationForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=150, label="الاسم الأول", required=True)
    last_name = forms.CharField(max_length=150, label="اسم العائلة", required=True)
    username = forms.CharField(max_length=150, label="اسم المستخدم", required=True, help_text="يمكن استخدام رقم الهاتف كاسم مستخدم")
    phone_number = forms.CharField(max_length=13, label="رقم الهاتف", required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="الجنس", required=True)
    
    # Doctor fields
    specialization = forms.CharField(max_length=100, label="التخصص", required=False)
    examination_type = forms.ChoiceField(choices=EXAMINATION_TYPE_CHOICES, label="نوع التعاقد", required=False)
    percentage_value = forms.FloatField(label="قيمة النسبة المئوية (%)", required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    price_value = forms.FloatField(label="المبلغ الثابت (لتقاسم الوقت)", required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add special classes for premium look
        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
        self.fields['examination_type'].widget.attrs.update({'class': 'form-select'})

    def clean(self):
        cleaned_data = super().clean()
        exam_type = cleaned_data.get("examination_type")
        percentage_val = cleaned_data.get("percentage_value")
        price_val = cleaned_data.get("price_value")

        if exam_type == 'percentage' and not percentage_val:
            self.add_error('percentage_value', 'يجب إدخال نسبة مئوية عند اختيار نوع التعاقد كنسبة.')
        elif exam_type == 'time_share' and not price_val:
            self.add_error('price_value', 'يجب إدخال المبلغ الثابت عند اختيار نوع التعاقد كتقاسم وقت.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        if commit:
            user.save()
            # Create or update the doctor profile
            Doctor.objects.update_or_create(
                user=user,
                defaults={
                    'specialization': self.cleaned_data.get('specialization'),
                    'examination_type': self.cleaned_data.get('examination_type'),
                    'percentage_value': self.cleaned_data.get('percentage_value'),
                    'price_value': self.cleaned_data.get('price_value'),
                }
            )
        return user


class ReceptionistCreationForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=150, label="الاسم الأول", required=True)
    last_name = forms.CharField(max_length=150, label="اسم العائلة", required=True)
    username = forms.CharField(max_length=150, label="اسم المستخدم", required=True, help_text="يمكن استخدام رقم الهاتف كاسم مستخدم")
    phone_number = forms.CharField(max_length=13, label="رقم الهاتف", required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="الجنس", required=True)
    
    # Receptionist fields
    salary = forms.FloatField(label="الراتب (ج.م)", required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    hire_date = forms.DateField(label="تاريخ التعيين", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

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
        user.role = 'receptionist'
        if commit:
            user.save()
            # Create or update the receptionist profile
            Receptionist.objects.update_or_create(
                user=user,
                defaults={
                    'salary': self.cleaned_data.get('salary'),
                    'hire_date': self.cleaned_data.get('hire_date'),
                }
            )
        return user
