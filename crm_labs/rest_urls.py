# Third party imports
from django.urls import path
from crm_labs import rest_views

urlpatterns = [
    path(r'home-dashobard/', rest_views.HomeDashboard.as_view()),
    # path(r'crm/login/', rest_views.LoginAPIView.as_view()),
]
