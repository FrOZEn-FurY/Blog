# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Local imports
from .forms import UserRegisterationForm, UserLoginForm
from Posts.models import PostModel


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
            User.objects.create_user(username=cd['username'], password=cd['password'], email=cd['email'])
            messages.success(request, _('You have registered successfully'), 'success')
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
        return render(request, self.template_name, {'user': user, 'posts': posts})

