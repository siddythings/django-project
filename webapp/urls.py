from django.contrib import admin
from django.urls import path
from webapp import views
urlpatterns = [
    path('category/', views.HomepageCategory.as_view()),
    path('packages/', views.Package.as_view()),
]
