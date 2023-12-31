from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users),
    path('get-rsa-key/', views.get_rsa_key),
    path('login/', views.login),
    path('email-two-factor-authentication/', views.email_two_factor_authentication),
    path('verify-email-two-factor-authentication/', views.verify_email_two_factory_authentication),
    path('face-recognition-factor/', views.face_recognition_factor),
    path('android-id/', views.android_id)
]   