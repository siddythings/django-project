# Third party imports
from django.urls import path
from users import rest_views

urlpatterns = [
    path(r'crm/otp/', rest_views.OTPAPIView.as_view()),
    path(r'crm/login/', rest_views.LoginAPIView.as_view()),
]
