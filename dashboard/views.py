from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from appointments.models import Appointment
from services.models import ServiceRecord
from staff.models import Doctor
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from patients.models import Patient

@login_required
def admin_dashboard(request):
    # Check if user is admin
    if not request.user.is_superuser and request.user.role != 'admin':
        return render(request, '403.html', status=403)

    # Filter logic
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    exam_type = request.GET.get('exam_type', 'all')
    
    today = timezone.now().date()
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = today
        
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = start_date # If only one date provided, it's a single day

    # Fetch data
    appointments = Appointment.objects.filter(date__date__range=[start_date, end_date]).exclude(status='cancelled')
    services = ServiceRecord.objects.filter(created_at__date__range=[start_date, end_date])
    
    # Summary Statistics
    total_app_revenue = appointments.aggregate(Sum('cost'))['cost__sum'] or 0
    total_service_revenue = services.aggregate(Sum('service__price'))['service__price__sum'] or 0
    total_revenue = total_app_revenue + total_service_revenue
    
    # Detailed Doctor Analytics
    doctors = Doctor.objects.all()
    if exam_type != 'all':
        doctors = doctors.filter(examination_type=exam_type)
        
    doctor_data = []
    
    total_doctor_share = 0
    total_clinic_share = 0
    
    for doctor in doctors:
        # Appointments for this doctor
        doc_apps = appointments.filter(doctor=doctor)
        doc_app_rev = doc_apps.aggregate(Sum('cost'))['cost__sum'] or 0
        
        # Services for this doctor
        doc_services = services.filter(doctor=doctor)
        doc_service_rev = doc_services.aggregate(Sum('service__price'))['service__price__sum'] or 0
        doc_service_share = doc_services.aggregate(Sum('doctor_amount'))['doctor_amount__sum'] or 0
        
        # Calculate Appointment Share
        if doctor.examination_type == 'percentage':
            percentage = doctor.percentage_value or 0
            doc_app_share = doc_app_rev * (percentage / 100)
        else:
            doc_app_share = doc_app_rev 
            
        doc_total_share = doc_app_share + doc_service_share
        doc_clinic_share = (doc_app_rev + doc_service_rev) - doc_total_share
        
        total_doctor_share += doc_total_share
        total_clinic_share += doc_clinic_share
        
        if doc_apps.count() > 0 or doc_services.count() > 0:
            doctor_data.append({
                'doctor': doctor,
                'app_count': doc_apps.count(),
                'app_revenue': doc_app_rev,
                'service_revenue': doc_service_rev,
                'doctor_share': doc_total_share,
                'clinic_share': doc_clinic_share,
                'type': doctor.get_examination_type_display()
            })
            
    # Detailed Service Analytics
    service_filtered = services
    if exam_type != 'all':
        service_filtered = services.filter(doctor__examination_type=exam_type)
        
    service_details = service_filtered.values(
        'service__name', 
        'doctor__user__first_name', 
        'doctor__user__last_name'
    ).annotate(
        count=Count('id'),
        total_price=Sum('service__price'),
        total_doctor_share=Sum('doctor_amount'),
        total_clinic_share=Sum('clinic_amount')
    ).order_by('-total_price')

    # Detailed Appointment (Consultation) Analytics
    app_details_filtered = appointments
    if exam_type != 'all':
        app_details_filtered = appointments.filter(doctor__examination_type=exam_type)
    
    appointment_details = app_details_filtered.values(
        'doctor__user__first_name', 
        'doctor__user__last_name',
        'doctor__examination_type'
    ).annotate(
        count=Count('id'),
        total_revenue=Sum('cost'),
    ).order_by('-total_revenue')

    context = {
        'page_title': 'لوحة تحكم المدير',
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_revenue': total_revenue,
        'total_app_revenue': total_app_revenue,
        'total_service_revenue': total_service_revenue,
        'total_doctor_share': total_doctor_share,
        'total_clinic_share': total_clinic_share,
        'app_count': appointments.count(),
        'service_count': services.count(),
        'doctor_data': doctor_data,
        'service_details': service_details,
        'appointment_details': appointment_details,
        'exam_type': exam_type,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def unified_search(request):
    # Check permissions: Admin or Receptionist
    if not request.user.is_superuser and request.user.role not in ['admin', 'receptionist']:
        return render(request, '403.html', status=403)

    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'patient')  # default to patient
    page_number = request.GET.get('page', 1)

    results = []
    
    if search_type == 'doctor':
        queryset = Doctor.objects.select_related('user').all()
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__phone_number__icontains=query) |
                Q(specialization__icontains=query)
            )
        results = queryset.order_by('user__first_name')
    else:  # patient
        queryset = Patient.objects.select_related('user').all()
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__phone_number__icontains=query)
            )
        results = queryset.order_by('-created_at')

    paginator = Paginator(results, 10)  # 10 results per page
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'البحث الموحد',
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
    }
    return render(request, 'dashboard/unified_search.html', context)