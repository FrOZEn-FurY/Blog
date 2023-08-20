# Django imports
from django.contrib import admin

# Local imports
from .models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    raw_id_fields = ('parent',)
    prepopulated_fields = {
        'slug': ('name',),
    }
