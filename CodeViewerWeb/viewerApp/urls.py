from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.info_viewer, name='search'),
    path('upload/', views.salary_update_excel, name='upload'),
]
