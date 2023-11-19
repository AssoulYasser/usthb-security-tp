from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('2fa/', views.email_two_factor_authentication)
]