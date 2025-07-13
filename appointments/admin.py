from django.contrib import admin
from .models import Appointment

from jalali_date.admin import ModelAdminJalaliMixin

@admin.register(Appointment)
class AppointmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('full_name', 'date', 'time', 'phone_number', 'status')
    list_filter = ('status', 'date')
    search_fields = ('full_name', 'phone_number')
    ordering = ('-date', 'time')