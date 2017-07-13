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
from django.db.models import Q
from django.http import QueryDict

from aptm import settings
from aptp.models import Follow
from accounts.models import Order
from .models import Event, EventDetail, HouseType
from accounts.models import Customer
from .forms import EventForm, EventDetailForm, CustomerForm, HouseTypeForm


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
    form_class = EventForm
    template_name = 'popup/event_create.html'


class EventDetailView(DetailView):
    '''
    活动详情
    '''
    model = Event
    template_name = 'popup/event_detail.html'


class EventUpdateView(DialogMixin, UpdateView):
    '''
    编辑活动信息
    '''
    model = Event
    fields = [f.name for f in model._meta.fields]
    template_name = 'popup/event_create.html'


class EventTermUpdateView(DialogMixin, UpdateView):
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

    def put(self, request):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        if id:
            obj = Event.get(id)
            obj.is_pub = not obj.is_pub
            obj.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class EventDelStatus(View):
    '''
    车位/房源  上架/下架
    '''

    def put(self, request,**kwargs):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        if id:
            obj = EventDetail.get(id)
            obj.status = not obj.status
            obj.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class EventDelDel(View):
    '''
    车位/房源  删除
    '''

    def delete(self, request):
        id = request.GET.get('id')
        if id:
            EventDetail.get(id).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class ImportPriceView(View):
    '''
    导入数据
    '''

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        if id:
            event = Event.get(id)
            file = request.FILES.get('file')
            path = default_storage.save(
                'price/price.xlsx',
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
                                                         total=ed[6],
                                                         event=event)
                eventdetail.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class ExportView(View):
    '''
    导出房价
    '''

    def get(self, request, pk):
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
            response['Content-Disposition'] = 'attachment;filename=eventdetail.xls'
            response.write(sio.getvalue())
            return response
        return JsonResponse({'msg': '内容为空！'})


class ExportCustomerView(View):
    '''
    导出认筹名单
    '''

    def get(self, request, pk):
        objs = Customer.objects.filter(event_id=pk)
        if objs:
            sheet = Workbook(encoding='utf-8')
            s = sheet.add_sheet('数据表')
            list = ['姓名', '手机号', '身份证号', '备注']
            col = 0
            for i in list:
                s.write(0, col, i)
                col += 1
            row = 1
            for obj in objs:
                s.write(row, 0, obj.realname)
                s.write(row, 1, obj.mobile)
                s.write(row, 2, obj.identication)
                s.write(row, 3, obj.remark)
                row += 1
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=customer.xls'
            response.write(sio.getvalue())
            return response
        return JsonResponse({'msg': '内容为空！'})


class ExportHouseHotView(View):
    '''
    导出房源热度统计
    '''

    def get(self, request):
        objs = EventDetail.objects.all()
        if objs:
            sheet = Workbook(encoding='utf-8')
            s = sheet.add_sheet('数据表')
            list = [
                '楼栋',
                '单元',
                '楼层',
                '房号',
                '是否已售',
                '原价',
                '线上总价',
                '收藏人数',
                '公测是否已售']
            col = 0
            for i in list:
                s.write(0, col, i)
                col += 1
            row = 1
            for obj in objs:
                s.write(row, 0, obj.building)
                s.write(row, 1, obj.unit)
                s.write(row, 2, obj.floor)
                s.write(row, 3, obj.room_num)
                s.write(row, 4, obj.is_sold)
                s.write(row, 5, obj.price)
                s.write(row, 6, obj.total)
                s.write(row, 7, Follow.objects.filter(eventdetail=obj).count())
                s.write(row, 8, Order.objects.get(eventdetail=obj).is_test)
                row += 1
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=fangyuanredu.xls'
            response.write(sio.getvalue())
            return response
        return JsonResponse({'msg': '内容为空！'})


class ExportBuyHotView(View):
    '''
    导出购房热度统计
    '''

    def get(self, request):
        objs = Order.all()
        if objs:
            sheet = Workbook(encoding='utf-8')
            s = sheet.add_sheet('数据表')
            list = [
                '姓名',
                '手机号',
                '证件号码',
                '同意协议时间',
                '收藏房间数',
                '访问热度',
                '公测选择房间',
                '公测订单时间',
                '开盘选择房间',
                '开盘订单时间']
            col = 0
            for i in list:
                s.write(0, col, i)
                col += 1
            row = 1
            for obj in objs:
                s.write(row, 0, obj.user.customer.realname)
                s.write(row, 1, obj.user.customer.mobile)
                s.write(row, 2, obj.user.customer.identication)
                s.write(row, 3, obj.user.customer.protime)
                s.write(row, 4, Follow.objects.filter(user=obj.user).count())
                s.write(row, 5, obj.eventdetail.visit_num)
                # s.write(row, 6, obj.)
                s.write(row, 7, obj.time)
                # s.write(row, 8, obj.)
                s.write(row, 9, obj.opentime)
                row += 1
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=fangyuanredu.xls'
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
    '''
    认筹名单列表
    '''
    template_name = 'customer_list.html'
    model = Customer

    def get_queryset(self):
        value = self.request.GET.get('value')
        if value:
            obj = self.model.objects.get(Q(realname=value) | Q(
                mobile=value) | Q(identication=value))
            if obj:
                return obj
            else:
                return JsonResponse({'msg': '没有匹配的内容！'})
        else:
            self.event = Event.get(self.kwargs['pk'])
            return self.model.objects.filter(event=self.event)

    def get_context_data(self):
        context = super(CustomListView, self).get_context_data()
        context['event'] = self.event
        return context


class CustomCreateView(DialogMixin, CreateView):
    '''
    添加认筹名单
    '''
    form_class = CustomerForm
    template_name = 'popup/customer_create.html'

    def get_initial(self):
        initial = super(CustomCreateView, self).get_initial()
        initial['event'] = Event.get(self.kwargs['pk'])
        return initial


class CustomerCountUpdateView(DialogMixin, UpdateView):
    '''
    修改可选套数
    '''
    template_name = 'popup/customer_count.html'
    model = Customer
    fields = ['count']


class DeleteCustomerView(View):
    '''
    删除认筹名单
    '''

    def post(self, request):
        id = request.GET.get('id')
        if id:
            Customer.get(id).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class HouseHeatView(View):
    '''
    房源热度统计
    '''
    def get(self, request, *args, **kwargs):
        queryset = EventDetail.all()
        et_list = [{'id': et.id,
                    'building': et.building,
                    'unit': et.unit,
                    'floor': et.floor,
                    'room_num': et.room_num,
                    'is_sold': et.is_sold,
                    'price': et.price,
                    'total': et.total,
                    'num': et.num,
                    'is_testsold': et.is_testsold
                    } for et in queryset]
        return JsonResponse({'success': True, "data": et_list})


class HouseTypeListView(ListView):
    '''
    户型列表
    '''
    template_name = 'housetype_list.html'
    model = HouseType
    fields = ['name', 'pic', 'num']

    def get_queryset(self):
        self.event = Event.get(self.kwargs['pk'])
        queryset = self.model.objects.filter(event=self.event)
        return queryset

    def get_context_data(self):
        context = super(HouseTypeListView, self).get_context_data()
        context['event'] = self.event
        return context


class HouseTypeCreateView(DialogMixin, CreateView):
    '''
    新建户型
    '''
    template_name = 'popup/housetype_create.html'
    form_class = HouseTypeForm

    def get_initial(self):
        initial = super(HouseTypeCreateView, self).get_initial()
        initial['event'] = Event.get(self.kwargs['pk'])
        return initial


class HouseTypeUpdateView(DialogMixin, UpdateView):
    '''
    修改户型
    '''
    template_name = 'popup/housetype_create.html'
    model = HouseType
    fields = ['name', 'pic', 'num']
