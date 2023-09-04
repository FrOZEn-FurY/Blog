# Django imports
from django.contrib import admin

# Local imports
from .models import FollowModel


@admin.register(FollowModel)
class FollowModelAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'date_followed')
    list_filter = ('date_followed',)
    raw_id_fields = ('follower', 'following')
