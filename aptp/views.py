
from django.views.generic.base import TemplateView
from apt.models import Event, EventDetail
from django.utils import timezone


class HomePageView(TemplateView):
    '''
    登录之后主页面
    '''
    template_name = 'homepage.html'

    def get_context_data(self, request, **kwargs):
        context = super(HomePageView, self).get_context_data()
        customer = request.user.username
        timenow = timezone.localtime(
            timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        objs = Event.objects.values(
            'name',
            'phone_num',
            'test_start',
            'test_end',
            'event_start',
            'event_end',
            'cover').filter(
            event_end__gte=timenow).filter(is_pub=True)
        context['customer'] = customer
        context['events'] = objs
        return context


class HouseDetailView(TemplateView):
    '''
    房子具体信息
    '''
    template_name = 'eventdel.html'

    def get_context_data(self, request, **kwargs):
        context = super(HouseDetailView, self).get_context_data()
        id = request.GET.get('id')  # 房子id号
        obj = EventDetail.objects.values(
            'batch',
            'house_type',
            'floor',
            'floor_area',
            'price',
            'is_sold').get(id)
        # 还缺少房子平面图
        context['eventdetail'] = obj
        return context


# class ListView(TemplateView):
#     template_name = 'eventdellist.html'
#     def get_context_data(self, **kwargs):
#         context=super(ListView,self).get_context_data()

