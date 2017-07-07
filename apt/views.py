
from django.shortcuts import resolve_url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from xlwt import Workbook
from io import BytesIO
from django.http import JsonResponse, HttpResponse

from .models import Event, EventDetail


class DialogMixin(object):
    def get_success_url(self):
        return resolve_url('dialog_success')


class EventListView(ListView):
    template_name = 'event_list.html'
    model = Event

    def get_queryset(self):
        return self.model.objects.order_by('-id')


class EventCreateView(DialogMixin, CreateView):
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


def ExportView(request):
    objs = EventDetail.objects.all()
    if objs:
        sheet = Workbook(encoding='utf-8')
        s = sheet.add_sheet('数据表')
        s.write(0, 0, '楼栋')
        s.write(0, 1, '单元')
        s.write(0, 2, '楼层')
        s.write(0, 3, '房号')
        s.write(0, 4, '原价')
        s.write(0, 5, '线上总价')
        row = 1
        for obj in objs:
            building = obj.building
            unit = obj.unit
            floor = obj.floor
            room_num = obj.room_num
            price = obj.price
            total = obj.total
            s.write(row, 0, building)
            s.write(row, 1, unit)
            s.write(row, 2, floor)
            s.write(row, 3, room_num)
            s.write(row, 4, price)
            s.write(row, 5, total)
            row += 1
        sio = BytesIO()
        sheet.save(sio)
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=export.xls'
        response.write(sio.getvalue())
        return response
    return JsonResponse({'msg': '内容为空！'})
