from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Event
# from .form import EventCreateForm


class EventListView(ListView):
    template_name = 'event_list.html'
    model = Event
    # paginate_by = 12

    def get_queryset(self):
        return self.model.objects.order_by('-id')


class EventCreateView(CreateView):
    model = Event
    fields = [f.name for f in model._meta.get_fields()]
    template_name = 'event_create.html'
    # form_class = EventCreateForm
