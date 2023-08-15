# Django imports
from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = 'Home/Home.html'

    def get(self, request):
        return render(request, self.template_name)