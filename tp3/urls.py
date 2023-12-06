from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users),
    path('login/', views.login),
    path('email-two-factor-authentication/', views.email_two_factor_authentication),
    path('verify-email-two-factor-authentication/', views.verify_email_two_factory_authentication),
]   