# Django imports
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models import Q

# Local imports
from .models import PostModel, CommentsModel, LikeModel
from .forms import PostCreationForm, AddCommentForm
from Categories.models import CategoryModel


class PostCreationView(LoginRequiredMixin, View):
    template_name = 'Posts/PostCreate.html'
    form_class = PostCreationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = PostModel(title=cd['title'], body=cd['body'], category=cd['category'])
            post.author = request.user
            post.slug = slugify(cd['title'], allow_unicode=True)
            post.save()
            messages.success(request, _('Your post has been created successfully'), 'success')
            return redirect('accounts:Profile', request.user.username)
        return render(request, self.template_name, {'form': form})


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'Posts/PostDetail.html'

    def get(self, request, post_category, post_slug):
        category = get_object_or_404(CategoryModel, slug=post_category)
        post = get_object_or_404(PostModel, slug=post_slug, category=category)
        ancestors = category.get_ancestors(include_self=True)
        conditions = Q(category=category)
        for ctgr in category.get_descendants():
            conditions |= Q(category=ctgr)
        recent = get_list_or_404(PostModel, conditions)
        recent.remove(post)
        comments = CommentsModel.objects.filter(post=post)
        liked = LikeModel.objects.filter(liker=request.user, post=post).exists()
        likes = LikeModel.objects.filter(liker=request.user, post=post).count()
        return render(request, self.template_name,
                      {'post': post, 'ancestors': ancestors, 'recent': recent[:3], 'comments': comments,
                       'Liked': liked, 'Likes': likes})


class PostDeleteView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.post = get_object_or_404(PostModel, slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.post.author != request.user:
            messages.warning(request, _("You can only delete your own posts"), 'danger')
            return redirect('Home:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.post.delete()
        messages.success(request, _('Your post has been deleted successfully'), 'success')
        return redirect('Home:Home')


class PostUpdateView(LoginRequiredMixin, View):
    template_name = 'Posts/PostUpdate.html'
    form_class = PostCreationForm

    def setup(self, request, *args, **kwargs):
        self.object = get_object_or_404(PostModel, slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.object.author != request.user:
            messages.warning(request, _('You can only update your own posts'), 'danger')
            return redirect('Home:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'form': form, 'post': self.object})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.slug = slugify(cd['title'], allow_unicode=True)
            post.save()
            messages.success(request, _('Your post has been updated successfully'), 'success')
            return redirect('Posts:PostDetail', post.slug)
        return render(request, self.template_name, {'form': form})


class AddCommentView(LoginRequiredMixin, View):
    template_name = 'Posts/AddComment.html'
    form_class = AddCommentForm

    def setup(self, request, *args, **kwargs):
        self.object = get_object_or_404(PostModel, slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.object.author:
            messages.warning(request, _("You can't add a comment to your post"), 'danger')
            return redirect('Posts:PostDetail', self.object.category, self.object.slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            messages.success(request, _('Your comment has been submitted successfully'), 'success')
            return redirect('Posts:PostDetail', self.object.category, self.object.slug)
        return render(request, self.template_name, {'form': form})


class AddReplyView(LoginRequiredMixin, View):
    template_name = 'Posts/AddComment.html'
    form_class = AddCommentForm

    def setup(self, request, *args, **kwargs):
        self.object = get_object_or_404(PostModel, slug=kwargs['post_slug'])
        self.comment = get_object_or_404(CommentsModel, pk=kwargs['comment_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = self.object
            reply.parent = self.comment
            reply.save()
            messages.success(request, _('Your reply has been submitted successfully'), 'success')
            return redirect('Posts:PostDetail', self.object.category, self.object.slug)
        return render(request, self.template_name, {'form': form})


class LikePostView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(PostModel, slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.post_object.author:
            messages.warning(request, _("You can't like your own posts"), 'danger')
            return redirect('Posts:PostDetail', self.post_object.category, self.post_object.slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        liked = LikeModel.objects.filter(liker=request.user, post=self.post_object).exists()
        if not liked:
            LikeModel.objects.create(liker=request.user, post=self.post_object)
            messages.success(request, _(f'You liked the post { self.post_object.title } successfully'), 'success')
        else:
            like = get_object_or_404(LikeModel, liker=request.user, post=self.post_object)
            like.delete()
            messages.success(request, _(f'You disliked the post { self.post_object.title } successfully'), 'success')
        return redirect('Posts:PostDetail', self.post_object.category, self.post_object.slug)
