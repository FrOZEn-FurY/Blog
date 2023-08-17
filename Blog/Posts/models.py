# Django imports
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Third party imports
from ckeditor.fields import RichTextField


class PostModel(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    title = models.CharField(
        max_length=75,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )
    body = RichTextField()
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.author} Posted {self.title}'

    def get_absolute_url(self):
        return reverse_lazy('Posts:PostDetail', args=(self.slug,))

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-date_created', 'date_updated')
