import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions
from .models import CustomUser, EmailVerification
from .serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        otp = str(random.randint(100000, 999999))
        EmailVerification.objects.create(user=user, otp_code=otp)

        send_mail(
            'Verify your email',
            f'Your verification code is: {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        # Optionally, you can return the OTP in the response for testing purposes

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
            verification = user.email_verification

            if verification.otp_code != code:
                return Response({"detail": "Invalid verification code."}, status=400)

            if verification.is_expired():
                return Response({"detail": "Code expired. Please request a new one."}, status=400)

            verification.is_verified = True
            verification.save()

            return Response({"message": "Email verified successfully."})

        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        except EmailVerification.DoesNotExist:
            return Response({"detail": "No verification pending."}, status=404)



class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if email is verified
            try:
                verification = user.email_verification
                if not verification.is_verified:
                    return Response({"detail": "Email not verified."}, status=status.HTTP_403_FORBIDDEN)
            except EmailVerification.DoesNotExist:
                return Response({"detail": "Email not verified."}, status=status.HTTP_403_FORBIDDEN)

            # If verified, issue tokens
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                access = response.data["access"]
                refresh = response.data["refresh"]

                response.set_cookie(
                    key='access_token',
                    value=access,
                    httponly=True,
                    secure=False,  
                    samesite='Lax'
                )
                response.set_cookie(
                    key='refresh_token',
                    value=refresh,
                    httponly=True,
                    secure=False,
                    samesite='Lax'
                )
                response.data = {
                    "message": "Login successful",
                    "access": access,
                    "refresh": refresh,
                    "user": UserSerializer(user).data
                }
            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class CookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'message': 'Token refreshed', 'access': access_token})
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            return response
        except Exception as e:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"message": f"Hello, {user.username}. You are authenticated."})


class CheckEmailExists(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({'exists': True}, status=200)
        return Response({'exists': False}, status=200)
