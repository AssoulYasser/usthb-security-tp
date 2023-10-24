from django.urls import path
from . import views

urlpatterns = [
    path('text_decryption/', views.text_decryption),
    path('image_steganography/encryption', views.image_steganography_encryption),
    path('image_steganography/decryption', views.image_steganography_decryption),
]
