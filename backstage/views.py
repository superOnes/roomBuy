from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse

from accounts.models import User


class LoginView(View):
    '''
    登录
    '''
    def get(self, request):
        return render(request, 'bms/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user.is_superuser:
            return redirect(reverse('bms_home'))
        messages.error(request, '用户名或密码不正确')
        return redirect(reverse('bms_login'))


class HomeListView(ListView):
    template_name = 'bms/home.html'
    model = User

    def get_queryset(self):
        return self.model.objects.filter(is_admin=True)
