from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('debug/<str:file>', logs, name='logs'),
]