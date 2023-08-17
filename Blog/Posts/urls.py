# Django imports
from django.urls import path

# Local imports
from . import views


app_name = 'Posts'
urlpatterns = [
    path('Create/', views.PostCreationView.as_view(), name='PostCreate'),
    path('Detail/<slug:post_slug>/', views.PostDetailView.as_view(), name='PostDetail'),
]
