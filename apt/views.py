import os
import base64
import qrcode
import xlrd
from xlwt import Workbook
from io import BytesIO
from copy import copy

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import resolve_url
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.http import QueryDict
from django.utils.decorators import method_decorator

from aptm import settings
from accounts.models import Order, Customer
from aptp.models import Follow
from .models import Event, EventDetail, HouseType
from accounts.decorators import admin_required
from .forms import (EventForm, EventDetailForm, CustomerForm, HouseTypeForm,
                    EventDetailSignForm)


class DialogMixin(object):
    def get_success_url(self):
        return resolve_url('dialog_success')


def url2qrcode(data):
    '''
    二维码
    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data(data)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    return base64.b64encode(image_stream)


@method_decorator(admin_required, name='dispatch')
class EventListView(ListView):
    '''
    活动列表
    '''
    template_name = 'event_list.html'
    model = Event

    def get_queryset(self):
        self.value = self.request.GET.get('value')
        queryset = self.model.get_all_by_company(self.request.user.company.id)
        if self.value:
            queryset = queryset.filter(Q(name__contains=self.value))
        for obj in queryset:
            obj.qr = url2qrcode(
                'http://%s/static/m/views/choiceHouse.html?id=%s' %
                (self.request.get_host(), str(
                    obj.id)))
            obj.save()
        return queryset

    def get_context_data(self):
        context = super(EventListView, self).get_context_data()
        context['value'] = self.value
        return context


@method_decorator(admin_required, name='dispatch')
class EventCreateView(DialogMixin, CreateView):
    '''
    新增活动
    '''
    form_class = EventForm
    template_name = 'popup/event_create.html'

    def get_initial(self):
        initial = super(EventCreateView, self).get_initial()
        initial['company'] = self.request.user.company
        return initial


@method_decorator(admin_required, name='dispatch')
class EventDetailView(DetailView):
    '''
    活动详情
    '''
    model = Event
    template_name = 'popup/event_detail.html'


@method_decorator(admin_required, name='dispatch')
class EventUpdateView(DialogMixin, UpdateView):
    '''
    编辑活动信息
    '''
    model = Event
    fields = [f.name for f in model._meta.fields]
    template_name = 'popup/event_create.html'


@method_decorator(admin_required, name='dispatch')
class EventTermUpdateView(DialogMixin, UpdateView):
    '''
    编辑协议
    '''
    model = Event
    fields = ['termname', 'term']
    template_name = 'popup/event_term.html'


@method_decorator(admin_required, name='dispatch')
class EventStatus(View):
    '''
    活动发布情况 发布/未发布
    '''

    def put(self, request):
        user = request.user
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        if not id:
            return JsonResponse({'success': False})
        obj = Event.get(id)
        obj.is_pub = not obj.is_pub
        obj.save()
        Event.objects.filter(
            company=user.company,
            is_pub=True).exclude(id=id).update(is_pub=False)
        return JsonResponse({'success': True})


@method_decorator(admin_required, name='dispatch')
class EventDetailListView(ListView):
    '''
    房源/车位列表
    '''
    template_name = 'eventdetail_list.html'
    model = EventDetail

    def get_queryset(self):
        self.value = self.request.GET.get('value')
        self.event = Event.get(self.kwargs['pk'])
        queryset = self.model.objects.filter(event=self.event).order_by('-id')
        if self.value:
            queryset = queryset.filter(
                Q(room_num__contains=self.value)).order_by('-id')
        return queryset

    def get_context_data(self):
        context = super(EventDetailListView, self).get_context_data()
        context['event'] = self.event
        context['value'] = self.value
        return context


@method_decorator(admin_required, name='dispatch')
class EventDetailCreateView(DialogMixin, CreateView):
    '''
    新增房间/车位
    '''
    template_name = 'popup/eventdetail_create.html'
    form_class = EventDetailForm

    def get_initial(self):
        initial = super(EventDetailCreateView, self).get_initial()
        initial['event'] = Event.get(self.kwargs['pk'])
        initial['current_user'] = self.request.user
        return initial


@method_decorator(admin_required, name='dispatch')
class EventDetailPriceUpdateView(DialogMixin, UpdateView):
    '''
    编辑线上总价
    '''
    template_name = 'popup/eventdetail_total.html'
    fields = ['unit_price']
    model = EventDetail


@method_decorator(admin_required, name='dispatch')
class EventDetailRemarkUpdateView(DialogMixin, UpdateView):
    '''
    情况描述
    '''
    template_name = 'popup/eventdetail_remark.html'
    model = EventDetail
    fields = ['remark', 'image']


@method_decorator(admin_required, name='dispatch')
class EventDetailSignUpdateView(DialogMixin, UpdateView):
    '''
    备注
    '''
    template_name = 'popup/eventdetail_sign.html'
    model = EventDetail
    form_class = EventDetailSignForm

    def get_initial(self):
        initial = super(EventDetailSignUpdateView, self).get_initial()
        initial['object'] = copy(self.object)
        return initial


@method_decorator(admin_required, name='dispatch')
class EventDetailHTUpdateView(DialogMixin, UpdateView):
    template_name = 'popup/eventdetail_ht.html'
    model = EventDetail
    fields = ['house_type']


@method_decorator(admin_required, name='dispatch')
class EventDetailStatus(View):
    '''
    车位/房源  上架/下架
    '''

    def put(self, request, **kwargs):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        if id:
            obj = EventDetail.get(id)
            obj.status = not obj.status
            obj.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@method_decorator(admin_required, name='dispatch')
class EventDetailDel(View):
    '''
    车位/房源  删除
    '''

    def post(self, request):
        id = request.POST.get('id')
        if id:
            EventDetail.get(id).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@method_decorator(admin_required, name='dispatch')
class ImportEventDetailView(View):
    '''
    导入车位房源
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
                etdtnum = len(EventDetail.objects.filter(event_id=id))
                num = request.user.house_limit - etdtnum
                if EventDetail.objects.filter(
                        event_id=id, building=ed[1],
                        unit=ed[2], floor=ed[3],
                        room_num=ed[4]).exists():
                    continue
                if num > 0:
                    eventdetail = EventDetail.objects.create(
                        building=ed[0],
                        unit=ed[1],
                        floor=ed[2],
                        room_num=ed[3],
                        unit_price=ed[4],
                        area=ed[5],
                        looking=ed[6],
                        term=ed[7],
                        event=event)
                    eventdetail.save()
                    num -= 1
            os.remove('media/price/price.xlsx')
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'msg': '传入数据超额！'})


@method_decorator(admin_required, name='dispatch')
class ExportEventDetailView(View):
    '''
    导出车位房源
    '''

    def get(self, request, pk):
        objs = EventDetail.objects.filter(event_id=pk)
        sheet = Workbook(encoding='utf-8')
        s = sheet.add_sheet('数据表')
        list = [
            '楼栋',
            '单元',
            '楼层',
            '房号',
            '面积单价',
            '建筑面积',
            '朝向',
            '使用年限']
        col = 0
        for i in list:
            s.write(0, col, i)
            col += 1
        if not objs:
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=\
                                               fangyuanxinxi.xls'
            response.write(sio.getvalue())
            return response
        row = 1
        for obj in objs:
            s.write(row, 0, obj.building)
            s.write(row, 1, obj.unit)
            s.write(row, 2, obj.floor)
            s.write(row, 3, obj.room_num)
            s.write(row, 4, obj.unit_price)
            s.write(row, 5, obj.area)
            s.write(row, 6, obj.looking)
            s.write(row, 7, obj.term)
            row += 1
        sio = BytesIO()
        sheet.save(sio)
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=\
                                           fangyuanxinxi.xls'
        response.write(sio.getvalue())
        return response


@method_decorator(admin_required, name='dispatch')
class CustomListView(ListView):
    '''
    认筹名单列表
    '''
    template_name = 'customer_list.html'
    model = Customer

    def get_queryset(self):
        self.value = self.request.GET.get('value')
        self.event = Event.get(self.kwargs['pk'])
        queryset = self.model.objects.filter(event=self.event).order_by('-id')
        if self.value:
            queryset = queryset.filter(Q(realname__icontains=self.value) |
                                       Q(mobile__icontains=self.value) |
                                       Q(identication__icontains=self.value)
                                       ).order_by('-id')
        return queryset

    def get_context_data(self):
        context = super(CustomListView, self).get_context_data()
        context['event'] = self.event
        context['value'] = self.value
        return context


@method_decorator(admin_required, name='dispatch')
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


@method_decorator(admin_required, name='dispatch')
class CustomerDeleteView(View):
    '''
    删除认筹名单
    '''

    def post(self, request):
        id = request.POST.get('id')
        if id:
            Customer.get(id).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@method_decorator(admin_required, name='dispatch')
class ExportCustomerView(View):
    '''
    导出认筹名单
    '''

    def get(self, request, pk):
        objs = Customer.objects.filter(event_id=pk)
        sheet = Workbook(encoding='utf-8')
        s = sheet.add_sheet('数据表')
        list = ['姓名', '手机号', '身份证号', '备注']
        col = 0
        for i in list:
            s.write(0, col, i)
            col += 1
        if not objs:
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename= \
                                               renchoumingdan.xls'
            response.write(sio.getvalue())
            return response
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
        response['Content-Disposition'] = 'attachment;filename= \
                                           renchoumingdan.xls'
        response.write(sio.getvalue())
        return response


@method_decorator(admin_required, name='dispatch')
class ExportHouseHotView(View):
    '''
    导出房源热度统计
    '''

    def get(self, request, pk):
        objs = EventDetail.objects.filter(event_id=pk)
        sheet = Workbook(encoding='utf-8')
        s = sheet.add_sheet('数据表')
        list = [
            '楼栋',
            '单元',
            '楼层',
            '房号',
            '是否已售',
            '面积单价',
            '建筑面积',
            '收藏人数',
            '公测是否已售']
        col = 0
        for i in list:
            s.write(0, col, i)
            col += 1
        if not objs:
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename= \
                                               fangyuanredu.xls'
            response.write(sio.getvalue())
            return response
        row = 1
        for obj in objs:
            s.write(row, 0, obj.building)
            s.write(row, 1, obj.unit)
            s.write(row, 2, obj.floor)
            s.write(row, 3, obj.room_num)
            if obj.is_sold:
                s.write(row, 4, '已售')
            else:
                s.write(row, 4, '未售')
            s.write(row, 5, obj.unit_price)
            s.write(row, 6, obj.area)
            s.write(row, 7, obj.follow_set.count())
            if obj.is_testsold:
                s.write(row, 8, '公测已售')
            else:
                s.write(row, 8, '公测未售')
            row += 1
        sio = BytesIO()
        sheet.save(sio)
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename= \
                                           fangyuanredu.xls'
        response.write(sio.getvalue())
        return response


@method_decorator(admin_required, name='dispatch')
class ExportBuyHotView(View):
    '''
    导出购房热度统计
    '''

    def get(self, request, pk):
        objs = Order.objects.filter(eventdetail__event_id=pk)
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
        if not objs:
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename= \
                                               goufangredu.xls'
            response.write(sio.getvalue())
            return response
        row = 1
        for obj in objs:
            s.write(row, 0, obj.user.customer.realname)
            s.write(row, 1, obj.user.customer.mobile)
            s.write(row, 2, obj.user.customer.identication)
            s.write(row, 3, obj.user.customer.protime)
            s.write(row, 4, obj.user.follow_set.count())
            s.write(row, 5, obj.eventdetail.visit_num)
            if obj.eventdetail.is_testsold:
                s.write(row, 6,
                        obj.eventdetail.building +
                        '楼' +
                        obj.eventdetail.unit +
                        '单元' +
                        str(obj.eventdetail.floor) +
                        '层' +
                        str(obj.eventdetail.room_num) + '号')
                s.write(row, 7, (obj.time).strftime("%Y/%m/%d %H:%M:%S"))
                s.write(row, 8, None)
                s.write(row, 9, None)
            else:
                s.write(row, 6, None)
                s.write(row, 7, None)
                s.write(row, 8,
                        obj.eventdetail.building +
                        '楼' +
                        obj.eventdetail.unit +
                        '单元' +
                        str(obj.eventdetail.floor) +
                        '层' +
                        str(obj.eventdetail.room_num) + '号')
                s.write(row, 9, (obj.time).strftime("%Y/%m/%d %H:%M:%S"))
            row += 1
        sio = BytesIO()
        sheet.save(sio)
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=goufangredu.xls'
        response.write(sio.getvalue())
        return response


@method_decorator(admin_required, name='dispatch')
class ExportOrderView(View):
    '''
    导出订单条目
    '''

    def get(self, request, **kwargs):
        id = request.GET.get('id')
        is_test = request.GET.get('is_test')
        value = request.GET.get('value')
        queryset = Order.objects.filter(
            eventdetail__event_id=id, is_test=is_test)
        if value:
            objs = queryset.filter(
                Q(user__customer__realname__icontains=value) |
                Q(user__customer__mobile__icontains=value) |
                Q(user__customer__identication__icontains=value))
        else:
            objs = queryset
        sheet = Workbook(encoding='utf-8')
        s = sheet.add_sheet('数据表')
        list = [
            '选房时间',
            '车位/房间号',
            '单价',
            '建筑面积',
            '认购者',
            '手机号',
            '证件号码',
            '认筹人备注',
            '状态']
        col = 0
        for i in list:
            s.write(0, col, i)
            col += 1
        if not objs:
            sio = BytesIO()
            sheet.save(sio)
            sio.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename= \
                                               daochudingdan.xls'
            response.write(sio.getvalue())
            return response
        row = 1
        for obj in objs:
            s.write(row, 0, obj.time.strftime("%Y/%m/%d %H:%M:%S"))
            s.write(row, 1, obj.eventdetail.room_num)
            s.write(row, 2, obj.eventdetail.unit_price)
            s.write(row, 3, obj.eventdetail.area)
            s.write(row, 4, obj.user.customer.realname)
            s.write(row, 5, obj.user.customer.mobile)
            s.write(row, 6, obj.user.customer.identication)
            s.write(row, 7, obj.user.customer.remark)
            if obj.eventdetail.is_sold:
                s.write(row, 8, '已售')
            else:
                s.write(row, 8, '未售')
            row += 1
        sio = BytesIO()
        sheet.save(sio)
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename= \
                                           daochudingdan.xls'
        response.write(sio.getvalue())
        return response


@method_decorator(admin_required, name='dispatch')
class HouseHeatView(View):
    '''
    房源热度统计
    '''

    def get(self, request, *args, **kwargs):
        event_id = request.GET.get('id')
        if event_id:
            queryset = EventDetail.objects.filter(event_id=event_id)
        else:
            last_event = Event.get_last_event(request.user.company.id)
            queryset = EventDetail.objects.filter(event_id=last_event)
        et_list = [{'id': et.id,
                    'building': et.building,
                    'unit': et.unit,
                    'floor': et.floor,
                    'room_num': et.room_num,
                    'is_sold': et.is_sold,
                    'unit_price': et.unit_price,
                    'area': et.area,
                    'num': et.follow_set.count(),
                    'is_testsold': et.is_testsold
                    } for et in queryset]
        return JsonResponse({'success': True, 'data': et_list})


@method_decorator(admin_required, name='dispatch')
class PurcharseHeatView(View):
    '''
    购房者热度统计
    '''

    def get(self, request, *args, **kwargs):
        event_id = request.GET.get('id')
        li = []
        if event_id:
            queryset = Customer.objects.filter(event_id=event_id)
        else:
            last_event = Event.get_last_event(request.user.company.id)
            queryset = Customer.objects.filter(event_id=last_event)
        for customer in queryset:
            testorder = customer.user.order_set.filter(is_test=True).first()
            openorder = customer.user.order_set.filter(is_test=False).first()
            follow = Follow.objects.filter(user_id=customer.user.id)
            customer.count = len(follow)
            ct_list = {'id': customer.id,
                       'name': customer.realname,
                       'mobile': customer.mobile,
                       'identication': customer.identication,
                       'protime': customer.protime.strftime('%Y-%m-%d %H:%M:%S')
                       if customer.protime else '',
                       'count': customer.count,
                       'testtime': '',
                       'testroom': '',
                       'opentime': '',
                       'openroom': ''
                       }
            time = []
            room = []
            if testorder:
                order = customer.user.order_set.filter(is_test=True)
                for td in order:
                    time.append(td.time.strftime("%Y/%m/%d %H:%M:%S"))
                    room.append(td.eventdetail.building +
                                td.eventdetail.unit +
                                str(td.eventdetail.floor) +
                                '层' +
                                str(td.eventdetail.room_num) +
                                '号')
                    ct_list['testtime'] = time
                    ct_list['testroom'] = room
            if openorder:
                order = customer.user.order_set.filter(is_test=False)
                for od in order:
                    time.append(od.time.strftime("%Y/%m/%d %H:%M:%S"))
                    room.append(od.eventdetail.building +
                                od.eventdetail.unit +
                                str(od.eventdetail.floor) +
                                '层' +
                                str(od.eventdetail.room_num) +
                                '号')
                    ct_list['opentime'] = time
                    ct_list['openroom'] = room
            li.append(ct_list)
        return JsonResponse({'success': True, 'data': li})


@method_decorator(admin_required, name='dispatch')
class GetEventView(View):
    '''
    获取活动列表
    '''

    def get(self, request, *args, **kwargs):
        event_list = Event.get_all_by_company(request.user.company.id)
        event = [{'id': et.id,
                  'name': et.name} for et in event_list]
        return JsonResponse({'success': True, 'data': event})


@method_decorator(admin_required, name='dispatch')
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


@method_decorator(admin_required, name='dispatch')
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


@method_decorator(admin_required, name='dispatch')
class HouseTypeUpdateView(DialogMixin, UpdateView):
    '''
    修改户型
    '''
    template_name = 'popup/housetype_create.html'
    form_class = HouseTypeForm
    model = HouseType

    def get_initial(self):
        initial = super(HouseTypeUpdateView, self).get_initial()
        initial['pk'] = self.kwargs['pk']
        return initial


@method_decorator(admin_required, name='dispatch')
class DeleteHouseTypeView(View):
    '''
    删除户型
    '''

    def post(self, request):
        id = request.POST.get('id')
        if id:
            EventDetail.objects.filter(
                house_type_id=id).update(house_type_id='')
            HouseType.get(id).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@method_decorator(admin_required, name='dispatch')
class HouseTypeRelatedView(View):
    '''
    一键关联
    '''

    def post(self, request):
        event_id = request.POST.get('event_id')
        event = Event.get(event_id)
        if event.type == Event.APT:
            eventdetails = event.eventdetail_set.all()
            for ed in eventdetails:
                house_type = HouseType.get_obj_by_num(str(ed.room_num)[-1],
                                                      event_id)
                if house_type and not ed.house_type:
                    ed.house_type = house_type
                    ed.save()
            return JsonResponse({'success': True, 'msg': '关联成功'})
        return JsonResponse({'success': False, 'msg': '暂不支持车位自动关联'})


@method_decorator(admin_required, name='dispatch')
class OrderListView(View):
    '''
    订单管理列表
    '''

    def get(self, request,):
        event_id = request.GET.get('id')
        is_test = request.GET.get('is_test')
        value = request.GET.get('value')
        if event_id and is_test:
            queryset = Order.objects.filter(
                eventdetail__event_id=event_id, is_test=is_test)
        else:
            last_event = Event.get_last_event(request.user.company.id)
            queryset = Order.objects.filter(
                eventdetail__event=last_event, is_test=0)
        if value:
            queryset = queryset.filter(
                Q(user__customer__realname__icontains=value) |
                Q(user__customer__mobile__icontains=value) |
                Q(user__customer__identication__icontains=value))
        if queryset:
            order_list = [{'id': od.id,
                           'time': od.time.strftime("%Y-%m-%d %H:%M:%S"),
                           'room_num': od.eventdetail.building +
                           '-' +
                           od.eventdetail.unit +
                           '-' +
                           str(od.eventdetail.floor) +
                           '-' +
                           str(od.eventdetail.room_num),
                           'unit_price': od.eventdetail.unit_price,
                           'area': od.eventdetail.area,
                           'realname': od.user.customer.realname,
                           'mobile': od.user.customer.mobile,
                           'identication': od.user.customer.identication,
                           'remark': od.user.customer.remark,
                           'status': od.eventdetail.status,
                           } for od in queryset]
            return JsonResponse({'success': True, 'data': order_list})
        return JsonResponse({'success': False})


@method_decorator(admin_required, name='dispatch')
class EventTVWall(TemplateView):
    template_name = 'wallList.html'

    def get_context_data(self, pk):
        context = super(EventTVWall, self).get_context_data()
        context['event_id'] = pk
        return context


@method_decorator(admin_required, name='dispatch')
class EventTVWallInfoView(View):

    def get(self, request, pk):
        result = []
        eventdetails = Event.get(pk).eventdetail_set.all()
        buildings = list(set(eventdetails.values_list('building', flat=True)))
        for b in buildings:
            units = eventdetails.filter(building=b).order_by('unit') \
                                .values_list('unit', flat=True)
            units = list(set(units))
            unit = []
            for u in units:
                rooms = eventdetails.filter(building=b, unit=u) \
                                    .order_by('room_num')
                room_dict = [{'id': r.id,
                              'room_num': r.room_num,
                              'is_sold': r.is_sold} for r in rooms]
                unit_dict = {'unit': u, 'rooms': room_dict}
                unit.append(unit_dict)
            building_dict = {'building': b, 'units': unit}
            result.append(building_dict)
        return JsonResponse({'response_state': 200, 'result': result})


@method_decorator(admin_required, name='dispatch')
class EventTVWallOrder(TemplateView):
    template_name = 'orderinfo.html'

    def get_context_data(self, pk):
        context = super(EventTVWallOrder, self).get_context_data()
        context['edid'] = pk
        return context


class EventTVWallOrderView(View):

    def get(self, request, pk):
        try:
            order = Order.objects.get(eventdetail_id=pk, is_test=False)
        except:
            return JsonResponse({'response_state': 400, 'msg': '未找到相关订单'})
        ed = order.eventdetail
        result = {
            'order_num': order.order_num,
            'order_date': order.time.strftime('%Y/%m/%d %H:%M:%S'),
            'user': order.user.customer.realname,
            'user_mobile': order.user.customer.mobile,
            'user_id': order.user.customer.identication,
            'house': ('%s楼-%s单元-%s') % (ed.building, ed.unit, ed.room_num),
            'event': ed.event.name,
            'house_type': ed.house_type.name if ed.house_type else '',
            'area': ed.area,
            'price': ed.unit_price,
        }
        return JsonResponse({'response_state': 200, 'result': result})
