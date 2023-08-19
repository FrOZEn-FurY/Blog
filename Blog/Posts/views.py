# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Local imports
from .models import PostModel
from .forms import PostCreationForm


class PostCreationView(LoginRequiredMixin, View):
    template_name = 'Posts/PostCreate.html'
    form_class = PostCreationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = PostModel(title=cd['title'], body=cd['body'])
            post.author = request.user
            post.slug = slugify(cd['title'], allow_unicode=True)
            print(post.slug)
            post.save()
            messages.success(request, _('Your post has been created successfully'), 'success')
            return redirect('accounts:Profile', request.user.username)
        return render(request, self.template_name, {'form': form})


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'Posts/PostDetail.html'

    def get(self, request, post_slug):
        post = get_object_or_404(PostModel, slug=post_slug)
        return render(request, self.template_name, {'post': post})
