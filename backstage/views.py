from django.shortcuts import render
from django.views.generic import View, ListView

from accounts.models import User


class LoginView(View):
    '''
    登录
    '''
    def get(self, request):
        return render(request, 'BMS/login.html')


class HomeListView(ListView):
    template_name = 'BMS/home.html'
    model = User

    def get_queryset(self):
        return self.model.objects.filter(is_admin=True)
