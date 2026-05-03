from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from .models import PasswordResetOTP
from .utils import generate_otp, send_otp_email
User = get_user_model()
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Account created successfully."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"message": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User with this email does not exist"}, status=404)

        PasswordResetOTP.objects.filter(user=user).delete()

        otp = generate_otp()
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_otp_email(user.email, otp)

        return Response({"message": "OTP sent successfully"}, status=200)

class VerifyOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"message": "Email and OTP are required"}, status=400)

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.get(user=user, otp=otp)
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"message": "Invalid OTP"}, status=400)

        if otp_obj.is_expired():
            otp_obj.delete()
            return Response({"message": "OTP expired"}, status=400)

        otp_obj.is_verified = True
        otp_obj.save()

        return Response({"message": "OTP verified successfully"}, status=200)
    
class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("password")

        if not email or not new_password:
            return Response({"message": "Email and password are required"}, status=400)

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, is_verified=True).latest("created_at")
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"message": "Unauthorized request"}, status=400)

        user.set_password(new_password)
        user.save()

        otp_obj.delete()

        return Response({"message": "Password reset successful"}, status=200)