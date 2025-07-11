from rest_framework import serializers
from .models import Appointment
from datetime import datetime

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        date = data.get('date')
        time = date.get('time')
        appointment_datetime = datetime.combine(date, time)
        if appointment_datetime < datetime.now():
            raise serializers.ValidationError("نمی‌توان نوبتی در زمان گذشته ثبت کرد.")
        return data