from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import Service, ServiceRecord
from patients.models import Patient
from staff.models import Doctor
from .forms import ServiceForm, ServiceRecordForm


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
        doctor_money = request.POST.get('doctor_money')
        clinic_money = request.POST.get('clinic_money')

        patient = get_object_or_404(Patient, pk=p_id)
        service = get_object_or_404(Service, pk=service_id)
        doctor = get_object_or_404(Doctor, pk=doctor_id)

        try:
            doctor_money_val = float(doctor_money) if doctor_money else 0.0
            clinic_money_val = float(clinic_money) if clinic_money else 0.0
        except ValueError:
            messages.error(request, 'الرجاء إدخال قيم عددية صالحة للمبالغ المالية.')
            return redirect('services:add_service', patient_id=patient.id)

        if doctor_money_val < 0 or clinic_money_val < 0:
            messages.error(request, 'لا يمكن أن تكون القيم المالية سالبة.')
            return redirect('services:add_service', patient_id=patient.id)

        if abs(service.price - (doctor_money_val + clinic_money_val)) > 0.01:
            messages.error(request, 'يجب أن يساوي مجموع نصيب الطبيب ونصيب العيادة سعر الخدمة.')
            return redirect('services:add_service', patient_id=patient.id)

        ServiceRecord.objects.create(
            patient=patient,
            service=service,
            doctor=doctor,
            doctor_money=doctor_money_val,
            clinic_money=clinic_money_val,
            created_by=request.user
        )
        messages.success(request, f"تم إضافة خدمة '{service.name}' للمريض بنجاح.")
        return redirect('patients:detail', pk=patient.id)

    active_services = Service.objects.filter(active=True)
    services_json = json.dumps({
        str(s.id): {'price': s.price}
        for s in active_services
    })
    context = {
        'page_title': 'إضافة خدمة جديدة',
        'patient': patient,
        'services': active_services,
        'doctors': Doctor.objects.all(),
        'services_json': services_json,
    }
    return render(request, 'services/add_service.html', context)

@login_required
@permission_required('services.add_service', raise_exception=True)
def create_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')

        Service.objects.create(
            name=name,
            price=price,
            created_by=request.user
        )
        messages.success(request, f"تم إنشاء الخدمة '{name}' بنجاح.")
        return redirect('dashboard:admin_dashboard')

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
    recent_records = service.service_records.all().order_by('-created_at')[:10]

    context = {
        'page_title': f'تفاصيل الخدمة: {service.name}',
        'service': service,
        'recent_records': recent_records,
    }
    return render(request, 'services/service_detail.html', context)


@login_required
def get_services_json(request):
    """Return active services as JSON for AJAX dropdowns."""
    query = request.GET.get('q', '')
    services = Service.objects.filter(active=True, name__icontains=query).order_by('name').values('id', 'name', 'price')
    return JsonResponse(list(services), safe=False)


@login_required
@permission_required('services.change_service', raise_exception=True)
def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            s = form.save(commit=False)
            s.updated_by = request.user
            s.save()
            messages.success(request, f"تم تحديث الخدمة '{s.name}' بنجاح.")
            return redirect('services:service_list')
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'page_title': f'تعديل الخدمة: {service.name}',
        'form': form,
        'service': service,
    }
    return render(request, 'services/update_service.html', context)


@login_required
@permission_required('services.change_servicerecord', raise_exception=True)
def update_service_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk)
    if request.method == 'POST':
        # Patient and doctor are fixed — take from hidden inputs (always the original record IDs)
        patient_id = request.POST.get('patient') or record.patient_id
        doctor_id  = request.POST.get('doctor')  or record.doctor_id
        service_id = request.POST.get('service')

        if not service_id:
            messages.error(request, 'يرجى اختيار خدمة.')
            return render(request, 'services/update_service_record.html', {'record': record})

        service = get_object_or_404(Service, pk=service_id)

        try:
            doctor_money = float(request.POST.get('doctor_money', 0))
            clinic_money = float(request.POST.get('clinic_money', 0))
        except (TypeError, ValueError):
            messages.error(request, 'الرجاء إدخال قيم مالية صالحة.')
            return render(request, 'services/update_service_record.html', {'record': record})

        if doctor_money < 0 or clinic_money < 0:
            messages.error(request, 'لا يمكن أن تكون القيم المالية سالبة.')
            return render(request, 'services/update_service_record.html', {'record': record})

        if abs(service.price - (doctor_money + clinic_money)) > 0.01:
            messages.error(request, 'يجب أن يساوي مجموع نصيب الطبيب ونصيب العيادة سعر الخدمة.')
            return render(request, 'services/update_service_record.html', {'record': record})

        record.patient_id  = patient_id
        record.doctor_id   = doctor_id
        record.service     = service
        record.doctor_money = doctor_money
        record.clinic_money = round(service.price - doctor_money, 2)
        record.updated_by  = request.user
        record.save()

        messages.success(request, 'تم تحديث سجل الخدمة بنجاح.')
        return redirect('patients:detail', pk=record.patient.id)

    context = {
        'page_title': f'تعديل سجل خدمة: {record.service.name}',
        'record': record,
    }
    return render(request, 'services/update_service_record.html', context)


@require_POST
@login_required
@permission_required('services.delete_service', raise_exception=True)
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    name = service.name
    service.delete()
    messages.success(request, f"تم حذف الخدمة '{name}' بنجاح.")
    return redirect('services:list')


@require_POST
@login_required
@permission_required('services.delete_servicerecord', raise_exception=True)
def delete_service_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk)
    patient_id = record.patient.id
    service_name = record.service.name
    record.delete()
    messages.success(request, f"تم حذف سجل خدمة '{service_name}' بنجاح.")
    return redirect('patients:detail', pk=patient_id)

