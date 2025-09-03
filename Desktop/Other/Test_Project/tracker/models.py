# tracker/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Impor model User bawaan Django

class Consumption(models.Model):
    # TAMBAHKAN FOREIGN KEY KE USER
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.amount} ml'