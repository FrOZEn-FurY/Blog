# Django imports
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Third party imports
from ckeditor_uploader.fields import RichTextUploadingField

# Local imports
from Categories.models import CategoryModel


class PostModel(models.Model):
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        related_name='category',
        default=None
    )
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
        max_length=150,
        unique=True,
        allow_unicode=True
    )
    body = RichTextUploadingField()
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
        ordering = ('-date_created', '-date_updated')
