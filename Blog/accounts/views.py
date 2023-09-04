# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Local imports
from .forms import UserRegisterationForm, UserLoginForm, EditProfileForm
from Posts.models import PostModel
from .models import FollowModel


class UserRegisterationView(View):
    template_name = 'accounts/Register.html'
    form_class = UserRegisterationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, _('It is non-sense to access this page while logged in'), 'danger')
            return redirect('Home:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(username=cd['username'], password=cd['password'], email=cd['email'])
            user.save()
            messages.success(request, _('You have registered successfully'), 'success')
            login(request, user)
            return redirect('Home:Home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    template_name = 'accounts/Login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, _('It is non-sense to access this page while logged in'), 'danger')
            return redirect('Home:Home')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, _('You have logged in successfully'), 'success')
                if not self.next:
                    return redirect('Home:Home')
                else:
                    return redirect(self.next)
            else:
                messages.error(request, _('User with the information given does not exists'), 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, _('You have logged out successfully'), 'success')
        return redirect('Home:Home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/Profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = PostModel.objects.filter(author=user)
        follow = FollowModel.objects.filter(follower=request.user, following=user).exists()
        return render(request, self.template_name, {'user': user, 'posts': posts, 'Follow': follow})


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/EditProfile.html'
    form_class = EditProfileForm

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.user:
            messages.warning(request, _('You can only edit your own profile'), 'danger')
            return redirect('accounts:Profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile info has been edited successfully'), 'success')
            return redirect('accounts:Profile', request.user.username)
        return render(request, self.template_name, {'form': form})


class DeleteUserView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.user:
            messages.warning(request, _('You can only delete your own account'), 'danger')
            return redirect('accounts:Profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        self.user.delete()
        messages.success(request, _('Your account has been deleted successfully'), 'success')
        return redirect('Home:Home')


class FollowView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.user == request.user:
            messages.warning(request, _("You can't follow yourself"), 'danger')
            return redirect('accounts:Profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        FollowModel.objects.create(follower=request.user, following=self.user)
        messages.success(request, _(f'You followed { self.user } successfully'), 'success')
        return redirect('accounts:Profile', self.user.username)


class UnfollowView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.user:
            messages.warning(request, _("You can't unfollow yourself"), 'danger')
            return redirect('accounts:Profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        follow = get_object_or_404(FollowModel, follower=request.user, following=self.user)
        follow.delete()
        messages.success(request, _(f'You unfollowed { self.user } successfully'), 'success')
        return redirect('accounts:Profile', self.user)


class FollowerView(LoginRequiredMixin, View):
    template_name = 'accounts/FollowerList.html'

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        follower_list = self.user.following.all()
        return render(request, self.template_name, {'list': follower_list, 'user': self.user})


class FollowingView(LoginRequiredMixin, View):
    template_name = 'accounts/FollowingList.html'

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        following_list = self.user.follower.all()
        return render(request, self.template_name, {'list': following_list, 'user': self.user})
