from django.urls import path
from . import views

urlpatterns = [
    path('text_decryption/rotation', views.rotation_decryption_request),
    path('text_decryption/caesar', views.caesar_decryption_request),
    path('text_decryption/mirror', views.mirror_decryption_request),
    path('text_decryption/affine', views.affine_decryption_request),
    path('image_steganography/encryption', views.image_steganography_encryption_request),
    path('image_steganography/decryption', views.image_steganography_decryption_request),
    path('password_attack', views.password_attack_request),
]
