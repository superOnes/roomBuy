from django.shortcuts import render
from django.views.generic import View


class ManagerView(View):
    '''
    登陆
    '''
    def get(self, request):
        return render(request, 'manager.html')
