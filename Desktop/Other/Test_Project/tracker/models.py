# tracker/models.py
from django.db import models
from django.utils import timezone

# Membuat tabel di database bernama 'Consumption'
class Consumption(models.Model):
    # Membuat kolom untuk menyimpan angka (jumlah air dalam ml)
    amount = models.IntegerField()

    # Membuat kolom untuk menyimpan tanggal dan waktu.
    # `default=timezone.now` artinya jika kita tidak memberikan waktu,
    # Django akan otomatis mengisinya dengan waktu saat ini.
    timestamp = models.DateTimeField(default=timezone.now)

    # Fungsi ini hanya untuk membantu kita di panel admin nanti,
    # agar data tampil dengan lebih mudah dibaca.
    def __str__(self):
        return f'{self.amount} ml at {self.timestamp.strftime("%Y-%m-%d %H:%M")}'