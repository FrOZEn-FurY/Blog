# Django imports
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Third party imports
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

# Local imports
from Categories.models import CategoryModel


class PostModel(models.Model):
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        related_name='category_posts',
        default=None
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_posts'
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
        return reverse_lazy('Posts:PostDetail', args=(self.category.slug, self.slug))

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-date_created', '-date_updated')


class CommentsModel(MPTTModel):
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        related_name='post_comment'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='parent_comment',
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    body = RichTextField(
        config_name="Comments"
    )

    def __str__(self):
        return f'{self.author} commented on {self.post}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-date_updated', '-date_created')


class LikeModel(models.Model):
    liker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liker'
    )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        related_name='post'
    )
    date_liked = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{ self.liker.username } liked { self.post.title }'

    class Meta:
        ordering = ('date_liked',)
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

