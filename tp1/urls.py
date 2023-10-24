from django.urls import path
from . import views

urlpatterns = [
    path('text_decryption/', views.text_decryption),
    path('image_steganography_encryption/', views.image_steganography_encryption)
]
