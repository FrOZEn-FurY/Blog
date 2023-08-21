# Django imports
from django.db import models
from django.urls import reverse

# Third party imports
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class CategoryModel(MPTTModel):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='Parent'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Categories:ShowCategoryPosts', args=(self.slug,))
