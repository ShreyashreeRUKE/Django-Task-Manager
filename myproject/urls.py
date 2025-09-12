from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adminshreyashree140/', admin.site.urls),
    path('', include('todoapp.urls')),  # 👈 this connects app URLs
]
