from rest_framework import serializers
from .models import Appointment

import jdatetime
from datetime import datetime, date, time as dtime


class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        date_str = self.initial_data.get("date")
        try:
            jdate = jdatetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            gdate = jdate.togregorian()
            data['date'] = gdate
        except:
            raise serializers.ValidationError({'date': 'تاریخ نامعتبر است. فرمت باید YYYY-MM-DD باشد.'})

        appointment_datetime = datetime.combine(data["date"], data["time"])
        if appointment_datetime < datetime.now():
            raise serializers.ValidationError("نمی‌توان نوبتی در زمان گذشته ثبت کرد.")
        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        gdate = instance.date
        jdate = jdatetime.date.fromgregorian(date=gdate)
        rep['date'] = jdate.strftime('%Y-%m-%d')
        return rep