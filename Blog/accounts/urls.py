# Django imports
from django.urls import path

# Local imports
from . import views


app_name = 'accounts'
urlpatterns = [
    path('Register/', views.UserRegisterationView.as_view(), name='Register'),
    path('Login/', views.UserLoginView.as_view(), name='Login'),
    path('Logout/', views.UserLogoutView.as_view(), name='Logout'),
    path('Profile/<str:username>/', views.UserProfileView.as_view(), name='Profile'),
]