# Django imports
from django.contrib import admin

# Local imports
from .models import PostModel


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated')
    prepopulated_fields = {
        'slug': ('title',),
    }
