# Django imports
from django.shortcuts import render
from django.views import View

# Local imports
from Posts.models import PostModel


class HomeView(View):
    template_name = 'Home/Home.html'

    def get(self, request):
        posts = PostModel.objects.all()
        return render(request, self.template_name, {'posts': posts})
