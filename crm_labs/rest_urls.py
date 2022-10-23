# Third party imports
from django.urls import path
from crm_labs import rest_views

urlpatterns = [
    path(r'home-dashobard/', rest_views.HomeDashboard.as_view()),
    path(r'booking/', rest_views.BookingAPIView.as_view()),
    path(r'packages/', rest_views.PackagesAPIView.as_view()),
    path(r'add-ons/', rest_views.AddOnServices.as_view()),
    path(r'package-instructions/', rest_views.PackageInstructionsAPIView.as_view()),
]
