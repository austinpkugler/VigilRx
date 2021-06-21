from django.urls import path

from . import views
from . import forms


urlpatterns = [
    path('', views.home, name='feed-home'),
    path('about/', views.about, name='feed-about'),
    path('prescribe/', views.prescribe, name='feed-prescribe')
]
