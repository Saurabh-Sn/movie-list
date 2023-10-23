"""
URL configuration for movies_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny, IsAuthenticated
admin.site.site_header = 'Movies List'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('movies_collection.urls')),
    path('api/docs/', include_docs_urls(title=admin.site.site_header, permission_classes=[AllowAny])),

]
