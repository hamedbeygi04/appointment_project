from django.urls import path
from .views import (
AppointmentListCreateAPIView,
AppointmentRetrieveUpdateDestroyAPIView,
RegisterView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/appointments/', AppointmentListCreateAPIView.as_view(), name='api_appointments'),
    path('api/appointment/<int:pk>/', AppointmentRetrieveUpdateDestroyAPIView.as_view(), name='api_appointment_detail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterView.as_view(), name='register'),
]