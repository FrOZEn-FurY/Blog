# Django imports
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Q

# Local imports
from .models import CategoryModel
from Posts.models import PostModel


class ShowCategoriesView(View):
    template_name = 'Categories/ShowCategory.html'

    def get(self, request):
        categories = CategoryModel.objects.all()
        return render(request, self.template_name, {'categories': categories})


class ShowCategoryPostsView(View):
    template_name = 'Categories/ShowPosts.html'

    def get(self, request, category_slug):
        category = get_object_or_404(CategoryModel, slug=category_slug)
        needed_categories = category.get_descendants(include_self=False)
        conditions = Q(category=category)
        for ctgr in needed_categories:
            conditions |= Q(category=ctgr)
        posts = PostModel.objects.filter(conditions).order_by('-date_created')
        return render(request, self.template_name, {'posts': posts})
