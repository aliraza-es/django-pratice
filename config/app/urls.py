from django.urls import path 
from . import views 
from app.views import UserRegistrationView, UserLoginView
from .views import UserProfileView, EmailLoginView

urlpatterns = [ 
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/login/', UserLoginView.as_view(), name='user_login'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/email-login/', EmailLoginView.as_view(), name='email_login'),
]