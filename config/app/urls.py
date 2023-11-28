from django.urls import path 
from . import views 
from app.views import UserRegistrationView, UserLoginView
from .views import UserProfileView, EmailLoginView
from .views import RequestPasswordResetView, CompletePasswordResetView

urlpatterns = [ 
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/login/', UserLoginView.as_view(), name='user_login'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/email-login/', EmailLoginView.as_view(), name='email_login'),
    path('api/password/reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('api/password/reset/complete/<uidb64>/<token>/', CompletePasswordResetView.as_view(), name='complete_password_reset'),
]