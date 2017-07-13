from django.views.generic.base import TemplateView
from apt.models import Event, EventDetail
from django.utils import timezone


class AppLoginView(TemplateView):
    template_name = 'aptp/login.html'


class AppEventDetailView(TemplateView):
    template_name = 'aptp/eventdetail.html'

    def get_context_data(self, pk):
        context = super(AppEventDetailView, self).get_context_data()
        context['event'] = Event.get(pk)
        return context


class AppEventDetailListView(TemplateView):
    template_name = 'aptp/house_list.html'

    def get_context_data(self, pk):
        context = super(AppEventDetailListView, self).get_context_data()
        context['event'] = Event.get(pk)
        context['object_list'] = EventDetail.objects.filter(event_id=pk)
        return context


class AppEventDetailDetailView(TemplateView):
    template_name = 'aptp/house_info.html'

    def get_context_data(self, pk):
        context = super(AppEventDetailDetailView, self).get_context_data()
        context['object'] = EventDetail.objects.get(id=pk)
        return context


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
        visit=EventDetail.get(id=id)
        visit.visit_num=visit.visit_num+1
        visit.save()
        # 还缺少房子平面图
        context['eventdetail'] = obj
        return context


# class ListView(TemplateView):
#     template_name = 'eventdellist.html'
#     def get_context_data(self, **kwargs):
#         context=super(ListView,self).get_context_data()
