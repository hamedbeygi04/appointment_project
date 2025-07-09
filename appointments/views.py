from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializers


class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all().order_by('-date', '-time')
    serializer_class = AppointmentSerializers


class AppointmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers