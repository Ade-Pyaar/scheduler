from django.urls import path

from .views import home, subscribe




urlpatterns = [
    path('', home, name='home'),
    path('subscribe/', subscribe, name='subscribe'),
]