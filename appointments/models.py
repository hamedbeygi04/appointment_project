from django.db import models


class Appointment(models.Model):
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