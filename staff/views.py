from django.http import JsonResponse
from django.db.models import Q
from .models import Doctor


from django.shortcuts import render
from django.utils import timezone
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required

@login_required
def get_doctor(request):
    query = request.GET.get('q', '')
    doctor = Doctor.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(specialization__icontains=query)
    )
    data = []
    for doctor in doctor:
        data.append({
            'id': doctor.id,
            'full_name': doctor.user.get_full_name(),
        })
    return JsonResponse(data, safe=False)
@login_required
def doctor_dashboard(request):
    # Check if user is a doctor
    if not hasattr(request.user, 'doctor'):
        return render(request, '403.html', status=403)
        
    doctor = request.user.doctor
    today = timezone.now().date()
    
    # Get today's appointments
    appointments = Appointment.objects.filter(
        doctor=doctor,
        date__date=today
    ).order_by('session_number')
    
    context = {
        'page_title': 'لوحة تحكم الطبيب',
        'doctor': doctor,
        'appointments': appointments,
        'today': today,
    }
    return render(request, 'staff/doctor_dashboard.html', context)
