#Django imports
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls', namespace='Home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('Posts/', include('Posts.urls', namespace='Posts')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('Categories/', include('Categories.urls', namespace='Categories'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
