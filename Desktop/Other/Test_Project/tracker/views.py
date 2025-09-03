# tracker/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Consumption
from django.contrib.auth.decorators import login_required # 1. JANGAN LUPA IMPORT INI

@login_required # 2. TAMBAHKAN DECORATOR INI
def index(request):
    # --- Bagian Logika untuk MENAMBAH data ---
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        if amount_str:
            amount = int(amount_str)
            # 3. PERBAIKI BARIS INI
            # Gunakan `amount` dari form dan `request.user` untuk user
            Consumption.objects.create(amount=amount, user=request.user)
        return redirect('index')

    # --- Bagian Logika untuk MENAMPILKAN data ---
    today = timezone.now().date()
    # 4. PERBAIKI QUERY INI DENGAN MENAMBAHKAN FILTER USER
    consumptions_today = Consumption.objects.filter(
        user=request.user,
        timestamp__date=today
    ).order_by('-timestamp')

    # Bagian ini sudah benar
    total_today_data = consumptions_today.aggregate(total=Sum('amount'))
    total_today = total_today_data['total'] or 0

    daily_goal = 2000
    progress_percentage = 0
    if total_today > 0:
        progress_percentage = (total_today / daily_goal) * 100
        if progress_percentage > 100:
            progress_percentage = 100

    context = {
        'consumptions': consumptions_today,
        'total_today': total_today,
        'daily_goal': daily_goal,
        'progress_percentage': progress_percentage,
    }
    
    return render(request, 'tracker/index.html', context)