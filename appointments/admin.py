from django.contrib import admin
from .models import Appointment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id' ,'full_name','user_id' , 'date', 'time', 'phone_number', 'status')
    list_filter = ('status', 'date')
    search_fields = ('full_name', 'phone_number')
    ordering = ('-date', 'time')

    def user_id(self, obj):
        return obj.user.id if obj.user else '-'
    user_id.short_description = 'User ID'

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')