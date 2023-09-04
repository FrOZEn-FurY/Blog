# Django imports
from django.db import models
from django.contrib.auth.models import User


class FollowModel(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    date_followed = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{ self.follower } is following { self.following }'

    class Meta:
        ordering = ('date_followed',)
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
