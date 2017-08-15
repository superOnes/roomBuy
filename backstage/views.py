from django.shortcuts import render
from django.views.generic import View


class LoginView(View):
    '''
    登录
    '''
    def get(self, request):
        return render(request, 'back/login.html')
