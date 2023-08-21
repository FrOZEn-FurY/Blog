# Django imports
from django.urls import path

# Local imports
from . import views


app_name = 'Categories'
urlpatterns = [
    path('', views.ShowCategoriesView.as_view(), name='Category'),
    path('<str:category_slug>/showposts/', views.ShowCategoryPostsView.as_view(), name='ShowCategoryPosts'),
]