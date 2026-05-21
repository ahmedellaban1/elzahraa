from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Medicine
from etc.choices import CONCENTRATION_UNIT_CHOICES

@login_required
@permission_required('medicines.view_medicine', raise_exception=True)
def list_medicines(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.all().order_by('-created_at')
    
    if query:
        medicines = medicines.filter(
            Q(trade_name__icontains=query) |
            Q(scientific_name__icontains=query)
        )
        
    context = {
        'page_title': 'إدارة الأدوية',
        'medicines': medicines,
        'query': query,
    }
    return render(request, 'medicines/list_medicines.html', context)

@login_required
@permission_required('medicines.add_medicine', raise_exception=True)
def add_medicine(request):
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
        return redirect('medicines:list_medicines')
        
    context = {
        'page_title': 'إضافة دواء جديد',
        'concentration_units': CONCENTRATION_UNIT_CHOICES,
    }
    return render(request, 'medicines/add_medicine.html', context)

@login_required
@permission_required('medicines.change_medicine', raise_exception=True)
def edit_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        trade_name = request.POST.get('trade_name')
        scientific_name = request.POST.get('scientific_name')
        concentration = request.POST.get('concentration')
        concentration_unit = request.POST.get('concentration_unit')
        
        medicine.trade_name = trade_name
        medicine.scientific_name = scientific_name
        medicine.concentration = concentration if concentration else None
        medicine.concentration_unit = concentration_unit
        medicine.save()
        
        messages.success(request, f"تم تعديل الدواء '{trade_name}' بنجاح.")
        return redirect('medicines:list_medicines')
        
    context = {
        'page_title': 'تعديل الدواء',
        'medicine': medicine,
        'concentration_units': CONCENTRATION_UNIT_CHOICES,
    }
    return render(request, 'medicines/edit_medicine.html', context)

@require_POST
@login_required
@permission_required('medicines.change_medicine', raise_exception=True)
def toggle_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.is_active = not medicine.is_active
    medicine.save()
    return JsonResponse({
        'status': 'success',
        'is_active': medicine.is_active,
        'message': f"تم {'تفعيل' if medicine.is_active else 'إلغاء تفعيل'} الدواء بنجاح."
    })


@login_required
def search_medicines(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(is_active=True)
    if query:
        medicines = medicines.filter(
            Q(trade_name__icontains=query) |
            Q(scientific_name__icontains=query)
        )
    
    results = []
    for med in medicines[:20]:
        display_name = med.trade_name
        if med.concentration:
            display_name += f" ({med.concentration} {med.get_concentration_unit_display()})"
        display_name += f" ({med.scientific_name})"
        
        results.append({
            'id': med.id,
            'text': display_name,
        })
        
    return JsonResponse({'results': results})