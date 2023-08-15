# Django imports
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Local imports
from .forms import UserRegisterationForm, UserLoginForm


class UserRegisterationView(View):
    template_name = 'accounts/Register.html'
    form_class = UserRegisterationForm

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
