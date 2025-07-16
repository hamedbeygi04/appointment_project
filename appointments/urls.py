from django.urls import path
from .views import (
    AppointmentListCreateAPIView,
    AppointmentRetrieveUpdateDestroyAPIView,
    RegisterView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    AvailableTimesView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/appointments/', AppointmentListCreateAPIView.as_view(), name='api_appointments'),
    path('api/appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyAPIView.as_view(), name='api_appointment_detail'),
    path("api/available-times/", AvailableTimesView.as_view(), name="available-times"),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterView.as_view(), name='register'),

    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]