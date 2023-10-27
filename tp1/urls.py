from django.urls import path
from . import views

urlpatterns = [
    path('text_decryption/rotation', views.rotation_decryption),
    path('text_decryption/caesar', views.caesar_decryption),
    path('text_decryption/mirror', views.mirror_decryption),
    path('image_steganography/encryption', views.image_steganography_encryption),
    path('image_steganography/decryption', views.image_steganography_decryption),
    path('password_attack', views.password_attack),
]
