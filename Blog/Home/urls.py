# Django imports
from django.urls import path

# Local imports
from . import views


app_name = 'Home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='Home'),
]