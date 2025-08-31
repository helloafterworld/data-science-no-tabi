# tracker/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Consumption # Impor model yang kita buat tadi

def index(request):
    # --- Bagian Logika untuk MENAMBAH data ---
    if request.method == 'POST':
        # Ambil data dari form yang bernama 'amount'
        amount_str = request.POST.get('amount')
        if amount_str: # Pastikan tidak kosong
            amount = int(amount_str)
            # Buat baris baru di tabel Consumption
            Consumption.objects.create(amount=amount)
        # Arahkan kembali ke halaman utama agar halaman me-refresh
        return redirect('index')

    # --- Bagian Logika untuk MENAMPILKAN data ---
    today = timezone.now().date()
    # Ambil semua data konsumsi yang timestamp-nya adalah hari ini
    consumptions_today = Consumption.objects.filter(timestamp__date=today).order_by('-timestamp')

    # Hitung total 'amount' dari data yang sudah difilter
    total_today_data = consumptions_today.aggregate(total=Sum('amount'))
    total_today = total_today_data['total'] or 0 # Jika belum ada data, totalnya 0

    # Siapkan data yang akan dikirim ke template
    context = {
        'consumptions': consumptions_today,
        'total_today': total_today,
    }

    # Tampilkan file 'index.html' dan kirim data 'context' ke dalamnya
    return render(request, 'tracker/index.html', context)