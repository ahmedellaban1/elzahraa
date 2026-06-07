from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentForm
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .models import Appointment, PrescriptionItem
from medicines.models import Medicine
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from etc.choices import (
    MEDICINE_DOSAGE_UNIT_CHOICES,
    MEDICINE_FREQUENCY_CHOICES,
    MEDICINE_DURATION_UNIT_CHOICES,
    MEDICINE_ROUTE_CHOICES,
    MEDICINE_NOTES
)

from django.utils.dateparse import parse_datetime

from django.utils import timezone

@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def index(request):
    return render(request, 'appointments/index.html', {'page_title': 'إدارة المواعيد'})

@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def list_appointments(request):
    status = request.GET.get('status', 'all')
    page_number = request.GET.get('page', 1)
    date_filter = request.GET.get('date')
    
    if date_filter:
        try:
            target_date = timezone.datetime.strptime(date_filter, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.now().date()
    else:
        target_date = timezone.now().date()
    
    appointments = Appointment.objects.filter(date__date=target_date).order_by('session_number')
    
    if status != 'all':
        appointments = appointments.filter(status=status)
    
    paginator = Paginator(appointments, 10) # 10 per page
    page_obj = paginator.get_page(page_number)
    
    html = render_to_string('appointments/partials/appointment_table.html', {
        'page_obj': page_obj,
        'current_status': status
    }, request=request)
    return HttpResponse(html)


@require_POST
@login_required
@permission_required('appointments.add_appointment', raise_exception=True)
def create_appointment(request):
    try:
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        date = parse_datetime(date_str)
        
        if not date:
            return JsonResponse({'status': 'error', 'message': 'تنسيق التاريخ غير صحيح'}, status=400)

        status = request.POST.get('status')
        appointment_type = request.POST.get('type', 'examination')
        room_number = request.POST.get('room_number')
        cost = request.POST.get('cost')
        doctor_money = request.POST.get('doctor_money')
        clinic_money = request.POST.get('clinic_money')
        notes = request.POST.get('notes')
        
        try:
            cost_val = float(cost) if cost else 0.0
            doctor_money_val = float(doctor_money) if doctor_money else 0.0
            clinic_money_val = float(clinic_money) if clinic_money else 0.0
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'الرجاء إدخال قيم عددية صالحة للمبالغ المالية.'}, status=400)

        if doctor_money_val < 0 or clinic_money_val < 0 or cost_val < 0:
            return JsonResponse({'status': 'error', 'message': 'لا يمكن أن تكون القيم المالية سالبة.'}, status=400)

        if abs(cost_val - (doctor_money_val + clinic_money_val)) > 0.01:
            return JsonResponse({'status': 'error', 'message': 'يجب أن يساوي مجموع نصيب الطبيب ونصيب العيادة التكلفة الإجمالية.'}, status=400)

        appointment = Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            status=status,
            type=appointment_type,
            room_number=room_number if room_number else None,
            cost=cost_val,
            doctor_money=doctor_money_val,
            clinic_money=round(cost_val - doctor_money_val, 2),
            notes=notes,
            created_by=request.user
        )
        return JsonResponse({'status': 'success', 'message': 'تم حفظ الموعد بنجاح'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@permission_required('appointments.add_prescriptionitem', raise_exception=True)
def add_prescription(request, appointment_id):
    # Check if user is a doctor
    if not hasattr(request.user, 'doctor'):
        return render(request, '403.html', status=403)
        
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Ensure this appointment belongs to the doctor
    if appointment.doctor != request.user.doctor:
        return render(request, '403.html', status=403)
        
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine')
        dosage = request.POST.get('dosage')
        dosage_unit = request.POST.get('dosage_unit')
        frequency = request.POST.get('frequency')
        duration = request.POST.get('duration')
        duration_unit = request.POST.get('duration_unit')
        route = request.POST.get('route')
        notes = request.POST.get('notes')
        
        PrescriptionItem.objects.create(
            appointment=appointment,
            medicine_id=medicine_id,
            dosage=dosage,
            dosage_unit=dosage_unit,
            frequency=frequency,
            duration=duration,
            duration_unit=duration_unit,
            route=route,
            notes=notes,
            created_by=request.user
        )
        messages.success(request, "تم إضافة الدواء للوصفة الطبية بنجاح.")
        return redirect('appointments:add_prescription', appointment_id=appointment.id)
        
    context = {
        'page_title': f'وصفة طبية: {appointment.patient.user.get_full_name()}',
        'appointment': appointment,
        'medicines': Medicine.objects.filter(is_active=True),
        'prescriptions': appointment.prescription_items.all().order_by('-created_at'),
        'dosage_units': MEDICINE_DOSAGE_UNIT_CHOICES,
        'frequencies': MEDICINE_FREQUENCY_CHOICES,
        'duration_units': MEDICINE_DURATION_UNIT_CHOICES,
        'routes': MEDICINE_ROUTE_CHOICES,
        'notes_choices': MEDICINE_NOTES,
    }
    return render(request, 'appointments/add_prescription.html', context)

@require_POST
@login_required
@permission_required('appointments.change_appointment', raise_exception=True)
def update_appointment_status(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
            appointment.status = new_status
            appointment.save()
            return JsonResponse({'status': 'success', 'message': f'تم تحديث الحالة إلى {appointment.get_status_display()}'})
        return JsonResponse({'status': 'error', 'message': 'حالة غير صالحة'}, status=400)
    except Appointment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'الموعد غير موجود'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
@login_required
@permission_required('appointments.change_appointment', raise_exception=True)
def save_appointment_notes(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Ensure this appointment belongs to the doctor (if user is a doctor)
    if hasattr(request.user, 'doctor') and appointment.doctor != request.user.doctor:
        return render(request, '403.html', status=403)
        
    notes = request.POST.get('notes', '')
    appointment.notes = notes
    appointment.save()
    messages.success(request, "تم حفظ الملاحظات الطبية بنجاح.")
    return redirect('appointments:add_prescription', appointment_id=appointment.id)


@login_required
@permission_required('appointments.view_prescriptionitem', raise_exception=True)
def print_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Ensure this appointment belongs to the doctor (if user is a doctor)
    if hasattr(request.user, 'doctor') and appointment.doctor != request.user.doctor:
        return render(request, '403.html', status=403)
        
    context = {
        'page_title': f'طباعة وصفة: {appointment.patient.user.get_full_name()}',
        'appointment': appointment,
        'prescriptions': appointment.prescription_items.all().order_by('created_at'),
    }
    return render(request, 'appointments/print_prescription.html', context)


@login_required
@permission_required('appointments.change_appointment', raise_exception=True)
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        patient_id   = request.POST.get('patient')
        doctor_id    = request.POST.get('doctor')
        date_str     = request.POST.get('date')
        status       = request.POST.get('status')
        appointment_type = request.POST.get('type', 'examination')
        room_number  = request.POST.get('room_number') or None
        notes        = request.POST.get('notes', '')

        date = parse_datetime(date_str)
        if not date:
            messages.error(request, 'تنسيق التاريخ غير صحيح.')
            return render(request, 'appointments/update_appointment.html', {'appointment': appointment})

        try:
            cost         = float(request.POST.get('cost'))
            doctor_money = float(request.POST.get('doctor_money'))
            clinic_money = float(request.POST.get('clinic_money'))
        except (TypeError, ValueError):
            messages.error(request, 'الرجاء إدخال قيم مالية صالحة.')
            return render(request, 'appointments/update_appointment.html', {'appointment': appointment})

        if cost < 0 or doctor_money < 0 or clinic_money < 0:
            messages.error(request, 'لا يمكن أن تكون القيم المالية سالبة.')
            return render(request, 'appointments/update_appointment.html', {'appointment': appointment})

        if abs(cost - (doctor_money + clinic_money)) > 0.01:
            messages.error(request, 'يجب أن يساوي مجموع نصيب الطبيب ونصيب العيادة التكلفة الإجمالية.')
            return render(request, 'appointments/update_appointment.html', {'appointment': appointment})

        appointment.patient_id   = patient_id
        appointment.doctor_id    = doctor_id
        appointment.date         = date
        appointment.status       = status
        appointment.type         = appointment_type
        appointment.room_number  = room_number
        appointment.cost         = cost
        appointment.doctor_money = doctor_money
        appointment.clinic_money = clinic_money
        appointment.notes        = notes
        appointment.updated_by   = request.user
        appointment.save()

        messages.success(request, 'تم تعديل الموعد بنجاح.')
        return redirect('appointments:index')

    context = {
        'page_title': f'تعديل الموعد #{appointment.session_number}',
        'appointment': appointment,
    }
    return render(request, 'appointments/update_appointment.html', context)