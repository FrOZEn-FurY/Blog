# Django imports
from django.contrib import admin

# Local imports
from .models import CategoryModel

# Third party imports
from mptt.admin import MPTTModelAdmin


@admin.register(CategoryModel)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'parent')
    raw_id_fields = ('parent',)
    prepopulated_fields = {
        'slug': ('name',),
    }
