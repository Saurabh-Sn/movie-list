from rest_framework import routers
from account.v1.api import RegistrationView, RequestContView
from django.urls import path, include
router = routers.DefaultRouter()
router.register('register', RegistrationView, 'register')
router.register('request-count', RequestContView, 'request_count')


urlpatterns = [
    path('', include(router.urls)),

]