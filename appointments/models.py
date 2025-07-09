from django.db import models

from django.contrib.auth.models import User


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', null=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=[
        ('pending', 'در انتظار'),
        ('confirmed', 'تایید شده'),
        ('canceled', 'لغو شده'),
    ], default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} | تاریخ: {self.date.strftime('%Y/%m/%d')} ساعت: {self.time.strftime('%H:%M')}"