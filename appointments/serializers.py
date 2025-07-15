from rest_framework import serializers
from .models import Appointment
from datetime import datetime

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        date = data.get("date")
        time = data.get("time")
        if date and time:
            appointment_datetime = datetime.combine(date, time)
            if appointment_datetime < datetime.now():
                raise serializers.ValidationError("نمی‌توان نوبتی در زمان گذشته ثبت کرد.")
        return data

    def update(self, instance, validated_data):
        validated_data['user'] =instance.user
        return super().update(instance, validated_data)