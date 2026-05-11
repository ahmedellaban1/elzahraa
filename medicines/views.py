from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine
from etc.choices import CONCENTRATION_UNIT_CHOICES

@login_required
def add_medicine(request):
    # Only admins can define medicines
    if not request.user.is_superuser and request.user.role != 'admin':
        return render(request, '403.html', status=403)
        
    if request.method == 'POST':
        trade_name = request.POST.get('trade_name')
        scientific_name = request.POST.get('scientific_name')
        concentration = request.POST.get('concentration')
        concentration_unit = request.POST.get('concentration_unit')
        
        Medicine.objects.create(
            trade_name=trade_name,
            scientific_name=scientific_name,
            concentration=concentration if concentration else None,
            concentration_unit=concentration_unit,
            created_by=request.user
        )
        messages.success(request, f"تم إضافة الدواء '{trade_name}' بنجاح.")
        return redirect('dashboard:admin_dashboard')
        
    context = {
        'page_title': 'إضافة دواء جديد',
        'concentration_units': CONCENTRATION_UNIT_CHOICES,
    }
    return render(request, 'medicines/add_medicine.html', context)