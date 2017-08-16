from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from accounts.models import User
from backstage.models import Province, City


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
        if user:
            if user.is_superuser:
                login(request, user)
                return redirect(reverse('home'))
        messages.error(request, '用户名或密码不正确')
        return redirect(reverse('login'))


class HomeListView(ListView):
    template_name = 'bms/home.html'
    model = User

    def get_queryset(self):
        return self.model.objects.filter(is_admin=True)


class CreateView(View):
    '''
    创建用户
    '''
    def get(self, request):
        return render(request, 'bms/createuser.html')

    def post(self, request):
        name = request.POST.get('username')
        house_limit = request.POST.get('house_limit')
        expire_date = request.POST.get('expire_date')


class GetProvinceView(View):
    '''
    省份列表
    '''

    def get(self, request, *args, **kwargs):
        province_list = Province.objects.all()
        province = [{'id': pv.id,
                  'name': pv.name} for pv in province_list]
        return JsonResponse({'success': True, 'data': province})


class GetCityView(View):
    '''
    市列表
    '''
    def get(self, request, *args, **kwargs):
        proid = request.GET.get('proid')
        city_list = City.objects.filter(province_id=proid)
        city = [{'id': ct.id,
                 'name': ct.name} for ct in city_list]
        return JsonResponse({'success': True, 'data': city})



