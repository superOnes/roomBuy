import os
import qrcode
from xlwt import Workbook
from io import BytesIO
import xlrd

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import resolve_url
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse, HttpResponse

from aptm import settings
from .models import Event, EventDetail
from accounts.models import Customer
from .forms import EventDetailForm, CustomerForm


class DialogMixin(object):
    def get_success_url(self):
        return resolve_url('dialog_success')


class EventListView(ListView):
    '''
    活动列表
    '''
    template_name = 'event_list.html'
    model = Event

    def get_queryset(self):
        return self.model.objects.order_by('-id')


class EventCreateView(DialogMixin, CreateView):
    '''
    新增活动
    '''
    model = Event
    fields = [f.name for f in model._meta.fields]
    template_name = 'popup/event_create.html'


class EventDetailView(DetailView):
    '''
    活动详情
    '''
    model = Event
    template_name = 'popup/event_detail.html'


class EventUpdateView(UpdateView):
    '''
    编辑活动信息
    '''
    model = Event
    fields = [f.name for f in model._meta.fields]
    template_name = 'popup/event_create.html'


class EventTermUpdateView(UpdateView):
    '''
    编辑协议
    '''
    model = Event
    fields = ['termname', 'term']
    template_name = 'popup/event_term.html'


class EventDetailListView(ListView):
    '''
    房源/车位列表
    '''
    template_name = 'eventdetail_list.html'
    model = EventDetail

    def get_queryset(self):
        self.event = Event.get(self.kwargs['pk'])
        return self.model.objects.filter(event=self.event).order_by('-id')

    def get_context_data(self):
        context = super(EventDetailListView, self).get_context_data()
        context['event'] = self.event
        return context


class EventDetailCreateView(DialogMixin, CreateView):
    '''
    新增房间/车位
    '''
    template_name = 'popup/eventdetail_create.html'
    form_class = EventDetailForm

    def get_initial(self):
        initial = super(EventDetailCreateView, self).get_initial()
        initial['event'] = Event.get(self.kwargs['pk'])
        return initial


class EventDetailTotalUpdateView(DialogMixin, UpdateView):
    '''
    编辑线上总价
    '''
    template_name = 'popup/eventdetail_total.html'
    fields = ['price', 'total']
    model = EventDetail


class EventDetailRemarkUpdateView(DialogMixin, UpdateView):
    '''
    情况描述
    '''
    template_name = 'popup/eventdetail_remark.html'
    model = EventDetail
    fields = ['remark', 'image']


class EventStatus(View):
    '''
    活动发布情况 发布/未发布
    '''

    def post(self, request):
        id = request.POST.get('id')
        if id:
            obj = Event.objects.get(id)
            obj.is_pub = not obj.is_pub
            obj.save()
            return JsonResponse({'success': True, 'msg': obj.is_pub})
        return JsonResponse({'success': False})


class EventDelStatus(View):
    '''
    车位/房源  上架/下架
    '''

    def post(self, request):
        id = request.POST.get('id')
        if id:
            obj = EventDetail.objects.get(id)
            obj.on_sale = not obj.on_sale
            obj.save()
            return JsonResponse({'success': True, 'msg': obj.on_sale})
        return JsonResponse({'success': False})


class EventDelDel(View):
    '''
    车位/房源  删除
    '''

    def post(self, request):
        id = request.POST.get('id')
        if id:
            obj = EventDetail.objects.get(id)
            obj.is_delete = True
            obj.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class ImportView(View):
    '''
    导入数据
    '''

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('f')
        path = default_storage.save(
            'tmp/somename.xlsx',
            ContentFile(
                file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        workdata = xlrd.open_workbook(tmp_file)
        sheet_name = workdata.sheet_names()[0]
        sheet = workdata.sheet_by_name(sheet_name)
        row = sheet.nrows
        col = sheet.ncols
        data = []
        for rx in range(1, row):
            li = []
            for cx in range(0, col):
                value = sheet.cell(rowx=rx, colx=cx).value
                li.append(value)
            data.append(li)
        for ed in data:
            eventdetail = EventDetail.objects.create(building=ed[1],
                                                     unit=ed[2],
                                                     floor=ed[3],
                                                     room_num=ed[4],
                                                     price=ed[5],
                                                     total=ed[6])
            eventdetail.save()
        os.remove('file/tmp/somename.xlsx')
        return JsonResponse({'success': True})


class ExportView(View):
    '''
    导出房价
    '''
    def get(self,request,pk):
        objs = EventDetail.objects.filter(event_id=pk)
        if objs:
            sheet = Workbook(encoding='utf-8')
            s = sheet.add_sheet('数据表')
            list = ['选房房源id', '楼栋', '单元', '楼层', '房号', '原价', '线上总价']
            col = 0
            for i in list:
                s.write(0, col, i)
                col += 1
            row = 1
            for obj in objs:
                s.write(row, 0, obj.id)
                s.write(row, 1, obj.building)
                s.write(row, 2, obj.unit)
                s.write(row, 3, obj.floor)
                s.write(row, 4, obj.room_num)
                s.write(row, 5, obj.price)
                s.write(row, 6, obj.total)
                row += 1
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=export.xls'
            response.write(sio.getvalue())
            return response
        return JsonResponse({'msg': '内容为空！'})


def url2qrcode(request, data):
    '''
    二维码
    '''
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    return response


class CustomListView(ListView):
    template_name = 'custom_list.html'
    model = Customer

    def get_queryset(self):
        self.event = Event.get(self.kwargs['pk'])
        return self.model.objects.filter(event=self.event)

    def get_context_data(self):
        context = super(CustomListView, self).get_context_data()
        context['event'] = self.event
        return context


class CustomCreateView(DialogMixin, CreateView):
    form_class = CustomerForm
    template_name = 'popup/custom_create.html'

    def get_initial(self):
        initial = super(CustomCreateView, self).get_initial()
        initial['event'] = Event.get(self.kwargs['pk'])
        return initial
