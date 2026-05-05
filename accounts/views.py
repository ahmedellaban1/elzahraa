from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home') # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"مرحباً بك مجدداً يا {user.first_name}!")
            return redirect('dashboard:home')
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
