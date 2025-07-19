from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import Appointment
from .serializers import AppointmentSerializers
from datetime import datetime, timedelta, time
from django.utils.timezone import make_aware

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser

from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        date = self.request.data.get("date")
        time = self.request.data.get("time")

        if not date or not time:
            raise ValidationError("تاریخ و ساعت الزامی هستند")

        try:
            selected_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            selected_dt = make_aware(selected_dt)
        except ValueError:
            raise ValidationError("فرمت تاریخ یا ساعت نادرست است")

        start_range = selected_dt - timedelta(hours=1)
        end_range = selected_dt + timedelta(hours=2)

        conflicts = Appointment.objects.filter(
            date=selected_dt.date(),
            time__gte=start_range.time(),
            time__lt=end_range.time()
        )

        if conflicts.exists():
            raise ValidationError("این بازه‌ی زمانی قبلاً رزرو شده است ❌")

        serializer.save(user=self.request.user)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff

class AppointmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializers
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

    def perform_update(self, serializer):
        date = self.request.data.get("date")
        time = self.request.data.get("time")

        if not date or not time:
            raise ValidationError("تاریخ و ساعت الزامی هستند")

        try:
            selected_dt = make_aware(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M"))
        except ValueError:
            raise ValidationError("فرمت تاریخ یا ساعت نادرست است")

        start_range = selected_dt - timedelta(hours=2)
        end_range = selected_dt + timedelta(hours=2)

        current_instance = self.get_object()

        conflicts = Appointment.objects.filter(
            date=selected_dt.date(),
            time__gte=start_range.time(),
            time__lt=end_range.time()
        ).exclude(id=current_instance.id)

        if conflicts.exists():
            raise ValidationError("در این بازه زمانی نوبت دیگری وجود دارد ❌")

        serializer.save()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "نام کاربری و رمز عبور الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "این نام کاربری قبلا ثبت شده است."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "ثبت نام با موفقیت انجام شد ✅"}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            return Response({'error': 'کاربر یافت نشد یا اطلاعات نادرست است'}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            subject='بازیابی رمز عبور',
            message=f'برای تغییر رمز عبور روی لینک زیر کلیک کنید:\n{reset_link}',
            from_email=None,
            recipient_list=[email],
        )
        return Response({'message': 'لینک بازیابی ارسال شد ✅'})


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({'error': 'لینک نامعتبر است'}, status=400)

        if default_token_generator.check_token(user, token):
            password = request.data.get('password')
            user.set_password(password)
            user.save()
            return Response({'message': 'رمز جدید ثبت شد ✅'})
        return Response({'error': 'توکن نامعتبر یا منقضی شده'}, status=400)


class AvailableTimesView(APIView):
    def get(self, request):
        date_str = request.GET.get("date")
        if not date_str:
            return Response({"error": "تاریخ ارسال نشده"}, status=400)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        reserved_times = Appointment.objects.filter(date=date).values_list("time", flat=True)
        all_times = [f"{h:02d}:00" for h in range(8, 23)]

        available = []
        for t in all_times:
            t_dt = datetime.strptime(t, "%H:%M")
            overlap = any(
                abs((t_dt.hour - rt.hour)) < 2
                for rt in reserved_times
            )
            if not overlap:
                available.append(t)

        return Response(available)