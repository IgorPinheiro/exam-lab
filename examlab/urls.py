from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name = 'users' ),
    path('exames/', include('exames.urls'), name = 'exames'),
]
