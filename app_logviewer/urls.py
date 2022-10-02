from turtle import down
from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('debug/<str:file>', logs, name='logs'),
    path('download_log/<str:file>', download_log, name='download_log'),
    path('delete_log/<str:file>', delete_log, name='delete_log'),
]