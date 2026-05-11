from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('staff/', include('staff.urls')),
    path('patients/', include('patients.urls')),
    path('', include('dashboard.urls')),
    path('services/', include('services.urls')),
    path('medicines/', include('medicines.urls')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
