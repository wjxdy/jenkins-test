from django.urls import path

from .views import health, hello

urlpatterns = [
    path('', hello, name='hello'),
    path('health/', health, name='health'),
]
