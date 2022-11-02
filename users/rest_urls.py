# Third party imports
from django.urls import path
from users import rest_views

urlpatterns = [
    #CRM login
    path(r'crm/otp/', rest_views.OTPAPIView.as_view()),
    path(r'crm/login/', rest_views.LoginAPIView.as_view()),
    
    #WebApp login
    path(r'user/otp/', rest_views.UserOTPAPIView.as_view()),
    path(r'user/login/', rest_views.UserLoginAPIView.as_view()),
]
