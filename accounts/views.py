from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard_router')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"مرحباً بك مجدداً يا {user.first_name}!")
            
            # Check for next url in query params
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
                
            # Perform role-based redirection via central router
            return redirect('dashboard:dashboard_router')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
    
    context = {
        'page_title': 'تسجيل الدخول | عيادات الزهراء'
    }
    return render(request, 'accounts/login.html', context)

def user_logout(request):
    auth_logout(request)
    context = {
        'page_title': 'تم تسجيل الخروج | عيادات الزهراء'
    }
    return render(request, 'accounts/logout.html', context)


@login_required
def user_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.phone_number = request.POST.get('phone_number', request.user.phone_number)
        request.user.save()
        messages.success(request, "تم تحديث بياناتك بنجاح!")
        return redirect('accounts:profile')
    
    context = {
        'page_title': 'الملف الشخصي | عيادات الزهراء'
    }
    return render(request, 'accounts/profile.html', context)

