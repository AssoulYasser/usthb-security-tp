from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tp1/', include('tp1.urls')),
    path('tp3/', include('tp3.urls'))
]
