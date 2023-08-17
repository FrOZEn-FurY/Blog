#Django imports
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls', namespace='Home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('Posts/', include('Posts.urls', namespace='Posts'))
]
