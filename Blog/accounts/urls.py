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
    path('Profile/Edit/<str:username>/', views.EditProfileView.as_view(), name='EditProfile'),
    path('Profile/Delete/<str:username>/', views.DeleteUserView.as_view(), name='DeleteUser'),
    path('Follow/<str:username>/', views.FollowView.as_view(), name='Follow'),
    path('UnFollow/<str:username>/', views.UnfollowView.as_view(), name='Unfollow'),
    path('<str:username>/Followers/', views.FollowerView.as_view(), name='Followers'),
    path('<str:username>/Following/', views.FollowingView.as_view(), name='Followings'),
]
