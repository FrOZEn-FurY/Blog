# Django imports
from django.urls import path

# Local imports
from . import views


app_name = 'Posts'
urlpatterns = [
    path('Create/', views.PostCreationView.as_view(), name='PostCreate'),
    path('Detail/<str:post_category>/<str:post_slug>/', views.PostDetailView.as_view(), name='PostDetail'),
    path('delete/<str:post_slug>/', views.PostDeleteView.as_view(), name='PostDelete'),
    path('update/<str:post_slug>/', views.PostUpdateView.as_view(), name='PostUpdate'),
]
