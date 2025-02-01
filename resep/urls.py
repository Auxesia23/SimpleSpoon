"""
URL configuration for resep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.handlers import (
    handler400, handler401, handler403, handler404,
    handler405, handler500, handler502, handler503
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('', include('main.urls')),
    path('', include('django_prometheus.urls')),
]

# Error Handlers
handler400 = 'main.handlers.handler400'  # Bad Request
handler401 = 'main.handlers.handler401'  # Unauthorized
handler403 = 'main.handlers.handler403'  # Forbidden
handler404 = 'main.handlers.handler404'  # Not Found
handler405 = 'main.handlers.handler405'  # Method Not Allowed
handler500 = 'main.handlers.handler500'  # Server Error
handler502 = 'main.handlers.handler502'  # Bad Gateway
handler503 = 'main.handlers.handler503'  # Service Unavailable
