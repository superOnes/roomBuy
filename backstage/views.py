from django.http import JsonResponse, request
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from accounts.models import User
from apt.models import Company
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        house_limit = request.POST.get('house_limit')
        expire_date = request.POST.get('expire_date')
        province = request.POST.get('province')
        city = request.POST.get('city')
        print(username, password, name, house_limit, expire_date, province, city)
        if username is None or password is None or name is None \
                or province is None or city is None:
            return JsonResponse({'successs': False})
        filteruser = User.objects.filter(username=username)
        if filteruser:
            return JsonResponse({'success': False, 'msg': '用户名已存在'})
        else:
            company = Company.objects.create(name=name,
                                             house_limit=house_limit,
                                             expire_date=expire_date
                                             if expire_date else '',
                                             province_id=province,
                                             city_id=city)
            User.objects.create_user(
                username=username,
                password=password,
                is_admin=True,
                company=company)
            return JsonResponse({'success': True, 'msg': '创建成功！'})


class ModifyUserView(View):
    '''
    修改用户信息
    '''
    def put(self, requests, *args, **kwargs):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        username = put.get('username')
        password = put.get('password')
        name = put.get('name')
        house_limit = put.get('house_limit')
        expire_date = put.get('expire_date')
        province = put.get('province')
        city = put.get('city')
        if id:
            user = User.get(id)
            company = user.company
            user.username = username
            user.password = password
            company.name = name
            company.house_limit = house_limit
            company.expire_date = expire_date
            company.province = province
            company.city = city
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeleteUserView(View):
        '''
        删除账户
        '''
        def delete(self, request):
            params = QueryDict(request.body, encoding=request.encoding)
            User.remove(params.get('id'))
            return JsonResponse({'success': True})


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



