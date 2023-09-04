# Django imports
from django.contrib import admin

# Local imports
from .models import PostModel, CommentsModel, LikeModel

# Third party imports
from mptt.admin import MPTTModelAdmin


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated')
    prepopulated_fields = {
        'slug': ('title',),
    }
    raw_id_fields = ('author', 'category')


@admin.register(CommentsModel)
class CommentModelAdmin(MPTTModelAdmin):
    list_display = ('parent', 'author', 'post', 'date_updated')
    list_filter = ('date_updated', 'date_created')
    raw_id_fields = ('author', 'post', 'parent')


@admin.register(LikeModel)
class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('liker', 'post', 'date_liked')
    list_filter = ('date_liked',)
    raw_id_fields = ('liker', 'post')
