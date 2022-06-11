from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from . import views

urlpatterns = [
    path('test/', views.test, name="test"),
    path('', views.index, name='index'),
]
