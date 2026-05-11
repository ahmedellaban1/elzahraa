from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from .forms import PatientCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.crypto import get_random_string
from services.models import Service, ServiceRecord
from appointments.models import Appointment, PrescriptionItem
from staff.models import Doctor


@login_required
def get_patient(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(
        Q(user__phone_number__startswith=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(user__phone_number__icontains=query)
    )
    data = []
    for patient in patients:
        data.append({
            'id': patient.id,
            'full_name': patient.user.get_full_name(),
            'phone': patient.user.phone_number
        })
    return JsonResponse(data, safe=False)

@login_required
def patient_detail(request, pk):
    # Check if user is staff or doctor
    if not request.user.is_superuser and request.user.role not in ['admin', 'doctor', 'receptionist']:
        return render(request, '403.html', status=403)
        
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all().order_by('-date')
    services = ServiceRecord.objects.filter(patient=patient).order_by('-created_at')
    
    # Get all prescriptions from all appointments
    prescriptions = PrescriptionItem.objects.filter(appointment__patient=patient).order_by('-created_at')
    
    # Handle temporary password display from session
    new_password = None
    if request.session.get('new_password') and request.session.get('reset_user_id') == patient.user.id:
        new_password = request.session.pop('new_password')
        request.session.pop('reset_user_id')

    context = {
        'page_title': f'بيانات المريض: {patient.user.get_full_name()}',
        'patient': patient,
        'appointments': appointments,
        'services': services,
        'prescriptions': prescriptions,
        'available_services': Service.objects.filter(active=True),
        'doctors': Doctor.objects.all(),
        'new_password': new_password,
    }
    return render(request, 'patients/patient_detail.html', context)

@login_required
def create_patient(request):
    # Check if user is staff or admin
    if not request.user.is_superuser and request.user.role not in ['admin', 'receptionist']:
        return render(request, '403.html', status=403)
        
    generated_password = None
    
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    # Generate a random password
                    generated_password = get_random_string(length=10)
                    user.set_password(generated_password)
                    user.created_by = request.user
                    user.save()
                    # Update the patient profile (it might have been created by a signal)
                    from .models import Patient
                    patient, created = Patient.objects.get_or_create(user=user)
                    patient.address = form.cleaned_data.get('address')
                    patient.birth_date = form.cleaned_data.get('birth_date')
                    patient.notes = form.cleaned_data.get('notes')
                    patient.save()
                    
                    messages.success(request, f"تم إنشاء حساب المريض بنجاح.")
                    # Pass the password to the context for display
                    return render(request, 'patients/create_patient.html', {
                        'form': form,
                        'generated_password': generated_password,
                        'new_user': user,
                        'page_title': 'تم إنشاء الحساب'
                    })
            except Exception as e:
                messages.error(request, f"حدث خطأ أثناء إنشاء الحساب: {str(e)}")
    else:
        form = PatientCreationForm()
        
    return render(request, 'patients/create_patient.html', {
        'form': form,
        'page_title': 'إضافة مريض جديد'
    })

@login_required
def reset_patient_password(request, pk):
    # Check if user is staff or admin
    if not request.user.is_superuser and request.user.role not in ['admin', 'receptionist']:
        return render(request, '403.html', status=403)
        
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    
    # Generate a new random password
    new_password = get_random_string(length=10)
    user.set_password(new_password)
    user.save()
    
    messages.success(request, f"تم إعادة تعيين كلمة المرور للمريض {user.get_full_name()} بنجاح.")
    
    # We'll pass the new password in the session to show it once
    request.session['new_password'] = new_password
    request.session['reset_user_id'] = user.id
    
    return redirect('patients:detail', pk=pk)
