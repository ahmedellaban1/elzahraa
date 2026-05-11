from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .models import Appointment, PrescriptionItem
from medicines.models import Medicine
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.dateparse import parse_datetime

from django.utils import timezone

@login_required
def index(request):
    return render(request, 'appointments/index.html', {'page_title': 'إدارة المواعيد'})

@login_required
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
def create_appointment(request):
    try:
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        date = parse_datetime(date_str)
        
        if not date:
            return JsonResponse({'status': 'error', 'message': 'تنسيق التاريخ غير صحيح'}, status=400)

        status = request.POST.get('status')
        room_number = request.POST.get('room_number')
        cost = request.POST.get('cost')
        notes = request.POST.get('notes')
        
        appointment = Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            status=status,
            room_number=room_number if room_number else None,
            cost=cost,
            notes=notes,
            created_by=request.user
        )
        return JsonResponse({'status': 'success', 'message': 'تم حفظ الموعد بنجاح'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
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
    }
    return render(request, 'appointments/add_prescription.html', context)

@require_POST
@login_required
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