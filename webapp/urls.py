from django.contrib import admin
from django.urls import path
from webapp import views
urlpatterns = [
    path('home-config/', views.ScreenPageConfig.as_view()),
    path('category/', views.HomepageCategory.as_view()),
    path('packages/', views.Package.as_view()),
    path('cities/', views.CityLabs.as_view()),
    path('labs/', views.Labs.as_view()),
    path('razorpay-key/', views.RazorpayKey.as_view()),



    path('shop/add-to-cart/<id>/', views.ShopAddToCart.as_view()),
    path('shop/cart/', views.GetCart.as_view()),
]
