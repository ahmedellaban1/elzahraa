from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Service, ServiceRecord
from patients.models import Patient
from staff.models import Doctor

@login_required
@permission_required('services.add_servicerecord', raise_exception=True)
def add_service(request, patient_id=None):
    if patient_id:
        patient = get_object_or_404(Patient, pk=patient_id)
    else:
        patient = None

    if request.method == 'POST':
        p_id = request.POST.get('patient_id')
        service_id = request.POST.get('service_id')
        doctor_id = request.POST.get('doctor_id')
        
        patient = get_object_or_404(Patient, pk=p_id)
        service = get_object_or_404(Service, pk=service_id)
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        
        ServiceRecord.objects.create(
            patient=patient,
            service=service,
            doctor=doctor,
            created_by=request.user
        )
        messages.success(request, f"تم إضافة خدمة '{service.name}' للمريض بنجاح.")
        return redirect('patients:detail', pk=patient.id)
    
    context = {
        'page_title': 'إضافة خدمة جديدة',
        'patient': patient,
        'services': Service.objects.filter(active=True),
        'doctors': Doctor.objects.all(),
    }
    return render(request, 'services/add_service.html', context)

@login_required
@permission_required('services.add_service', raise_exception=True)
def create_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        clinic_percentage = request.POST.get('clinic_percentage')
        
        Service.objects.create(
            name=name,
            price=price,
            clinic_percentage=clinic_percentage,
            created_by=request.user
        )
        messages.success(request, f"تم إنشاء الخدمة '{name}' بنجاح.")
        return redirect('dashboard:admin_dashboard') # Or a service list page if it exists
        
    context = {
        'page_title': 'تعريف خدمة جديدة',
    }
    return render(request, 'services/create_service.html', context)

@login_required
@permission_required('services.view_service', raise_exception=True)
def service_list(request):
    services = Service.objects.all().order_by('name')
    context = {
        'page_title': 'قائمة الخدمات',
        'services': services,
    }
    return render(request, 'services/service_list.html', context)

@login_required
@permission_required('services.view_service', raise_exception=True)
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    # Get recent records for this service
    recent_records = service.service_records.all().order_by('-created_at')[:10]
    
    context = {
        'page_title': f'تفاصيل الخدمة: {service.name}',
        'service': service,
        'recent_records': recent_records,
    }
    return render(request, 'services/service_detail.html', context)
