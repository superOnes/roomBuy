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


class AppHouseSuccessView(TemplateView):
    template_name = 'aptp/house_success.html'


class AppOrderListView(TemplateView):
    template_name = 'aptp/order_list.html'


class AppOrderInfoView(TemplateView):
    template_name = 'aptp/order_info.html'
