from django.views.generic import ListView
from .models import Event


class EventListView(ListView):
    template_name = 'event_list.html'
    model = Event
    # paginate_by = 12

    def get_queryset(self):
        return self.model.objects.order_by('-id')
