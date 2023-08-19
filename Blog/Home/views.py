# Django imports
from django.shortcuts import render
from django.views import View
from django.db.models import Q

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
        return render(request, self.template_name, {'posts': posts, 'form': form})
