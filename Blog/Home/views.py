# Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

# Local imports
from Posts.models import PostModel
from .forms import SearchForm


class HomeView(View):
    template_name = 'Home/Home.html'
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        search = request.GET.get('search', None)
        if search:
            posts = PostModel.objects.filter(title__contains=search)
        else:
            posts = PostModel.objects.all()
        posts_pages = Paginator(posts, 20)
        page_number = int(request.GET.get('page', 1))
        if page_number < 1 or page_number > posts_pages.num_pages:
            messages.warning(request, _("The requested page does not exists"), 'danger')
            return redirect('Home:Home')
        return render(request, self.template_name, {
            'posts': posts_pages.page(page_number),
            'form': form,
        })
