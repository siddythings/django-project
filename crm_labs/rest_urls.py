# Third party imports
from django.urls import path
from crm_labs import rest_views

urlpatterns = [
    path(r'home-dashobard/', rest_views.HomeDashboard.as_view()),
    path(r'booking/', rest_views.BookingAPIView.as_view()),
]
