from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from .serializers import UserProfileSerializer
from .models import UserProfile
from .serializers import EmailLoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            message = f'User {username} logged in successfully.'

            return Response({
                'message': message,
                'bearer_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = self.get_user_profile(request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    # def patch(self, request):
    #     user_profile = self.get_user_profile(request.user)
    #     serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user_profile(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # Create a new profile if it doesn't exist
            return UserProfile.objects.create(user=user)


class EmailLoginView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            
            user = authenticate(
                request,
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                message = f'Logged in successfully.'

                return Response({
                    'message': message,
                    'bearer_token': access_token,
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

# class RequestPasswordResetView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')

#         # Check if the email exists in the database
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Generate a token for password reset
#         uidb64 = urlsafe_base64_encode(force_bytes(user.id))
#         token = PasswordResetTokenGenerator().make_token(user)

#         # Create the reset link
#         reset_url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

#         # Send the reset link to the user's email
#         send_mail(
#             'Password Reset',
#             f'Click the following link to reset your password: {reset_url}',
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             fail_silently=False,
#         )

#         return Response({'detail': 'Password reset link sent'}, status=status.HTTP_200_OK)


# class CompletePasswordResetView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=uid)

#             # Check if the token is valid
#             if PasswordResetTokenGenerator().check_token(user, token):
#                 # Set a new password
#                 password = request.data.get('password')
#                 user.set_password(password)
#                 user.save()

#                 # Revoke existing refresh tokens
#                 RefreshToken.for_user(user).blacklist()

#                 return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({'detail': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a token for password reset
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        # Create the reset link
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

        # Send the reset link to the user's email
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({'detail': 'Password reset link sent'}, status=status.HTTP_200_OK)


class CompletePasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)

            # Check if the token is valid
            if PasswordResetTokenGenerator().check_token(user, token):
                # Set a new password
                password = request.data.get('password')
                user.set_password(password)
                user.save()
                # Blacklist existing refresh tokens
                refresh_tokens = RefreshToken.objects.filter(user=user)
                for token in refresh_tokens:
                    token.blacklist()

                return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)
