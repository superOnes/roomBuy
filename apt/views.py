from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Event, EventDetail


class EventListView(ListView):
    template_name = 'event_list.html'
    model = Event

    def get_queryset(self):
        return self.model.objects.order_by('-id')


class EventCreateView(CreateView):
    model = Event
    fields = [f.name for f in model._meta.get_fields()]
    template_name = 'event_create.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'popup/event_detail.html'


class EventUpdateView(UpdateView):
    model = Event
    fields = [f.name for f in model._meta.get_fields()]
    template_name = 'event_create.html'


class EventTermUpdateView(UpdateView):
    model = Event
    fields = ['term']
    template_name = 'popup/event_term.html'


class EventDetailListView(ListView):
    template_name = 'eventdetail_list.html'
    model = EventDetail

    def get_queryset(self):
        return self.model.objects.order_by('-id')


class EventDetailTotalUpdateView(UpdateView):
    '''
    修改线上总价
    '''
    template_name = 'popup/eventdetail_total.html'
    fields = ['total']
    model = EventDetail
