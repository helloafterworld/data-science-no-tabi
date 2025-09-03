# Test_Project/urls.py
from django.contrib import admin
# Jangan lupa tambahkan `include`
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Arahkan semua request dari URL kosong ('') ke file urls.py milik aplikasi tracker
    path('', include('tracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]