from django.urls import path
from .views import (
AppointmentListCreateAPIView,
AppointmentRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('api/appointments/', AppointmentListCreateAPIView.as_view(), name='api_appointments'),
    path('api/appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyAPIView.as_view(), name='api_appointment_detail'),
]