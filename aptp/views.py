import time

from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from apt.models import Event, EventDetail
from aptp.models import Follow
from accounts.models import Order
from accounts.decorators import customer_login_required, customer_login_time


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailView(View):
    '''
    显示活动
    '''

    def get(self, request, pk):
        obj = Event.get(pk)
        value = [{'test_start': obj.test_start,
                  'test_ent': obj.test_end,
                  'event_start': obj.event_start,
                  'event_end': obj.event_end,
                  'notice': obj.notice,
                  'description': obj.description,
                  'tip': obj.tip,
                  'name': obj.name,
                  'plane_graph': obj.plane_graph.url,
                  }]
        context = {}
        context['objects'] = value
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailListView(View):
    '''
    车位/房源 楼号列表
    '''

    def get(self, request, pk):
        eventobj = Event.get(pk)
        context = {}
        eventdetobj = EventDetail.objects.filter(event_id=pk)
        buildinglist = []
        for obj in eventdetobj:
            buildinglist.append((obj.building))
        value = [{
            'event_name': eventobj.name,
            'customer_count': eventobj.customer_set.count(),
            'event_start': (eventobj.event_start).strftime("%Y/%m/%d %H:%M:%S"),
            'building': list(set(buildinglist)),
        }]
        context['objects'] = value
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailUnitListView(View):
    '''
    车位/房源 单元列表
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        building = request.GET.get('building')
        context = {}
        eventdetobj = EventDetail.objects.filter(
            building=building, event_id=eventid)
        unitlist = []
        for obj in eventdetobj:
            unitlist.append((obj.unit))
        value = [{
            'unit': list(set(unitlist))
        }]
        context['objects'] = value
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailHouseListView(View):
    '''
    车位/房源 房号列表
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        building = request.GET.get('building')
        unit = request.GET.get('unit')
        context = {}
        eventdetobj = EventDetail.objects.filter(
            event_id=eventid, building=building, unit=unit)
        room_num_list = []
        for obj in eventdetobj:
            value = [{
                'house': obj.id,
                'floor_room_num': obj.floor + '-' + obj.room_num,
                'is_sold': obj.is_sold,
            }]
            room_num_list.append(value)
        context['objects'] = room_num_list
        return JsonResponse(context)


@method_decorator(customer_login_time, name='dispatch')
@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailHouseInfoView(View):
    '''
    车位/房源 详情
    '''

    def get(self, request):
        user = request.user
        house = request.GET.get('house')
        eventdetobj = EventDetail.get(house)
        test = True if time.strftime('%Y%m%d %H:%M:%S') <= eventdetobj.event.test_end.strftime(
            '%Y%m%d %H:%M:%S') else False
        try:
            Follow.objects.get(user=request.user, eventdetail=eventdetobj)
        except BaseException:
            is_followed = False,
        else:
            is_followed = True,
        value = [{
            'event': user.customer.event.name,
            'realname': user.customer.realname,
            'mobile': user.customer.mobile,
            'identication': user.customer.identication,
            'building_unit': eventdetobj.building +
            '-' +
            eventdetobj.unit +
            '-' +
            eventdetobj.floor +
            '-' + house,
            'total': '***' if test and not eventdetobj.event.test_price else eventdetobj.total,
            'house_type': '三室两厅',  # 这里还需要改
            'pic': '这是图片',  # 这里需要改
            'floor': eventdetobj.floor,
            'area': eventdetobj.area if eventdetobj.event.covered_space else '***',
            'unit_price': eventdetobj.unit_price if eventdetobj.event.covered_space_price else '***',
            'looking': eventdetobj.looking,
            'term': eventdetobj.term,
            'is_sold': eventdetobj.is_sold,
            'is_followed': is_followed,
        }]

        context = {}
        context['objects'] = value
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AddFollow(View):
    '''
    添加收藏
    '''

    def post(self, request):
        house = request.POST.get('house')
        user = request.user
        try:
            eventdetail = EventDetail.get(house)
            if not Follow.objects.filter(
                    user=user,
                    eventdetail=eventdetail):
                if user.follow_set.count() < user.customer.event.follow_num:
                    Follow.objects.create(
                        user=request.user, eventdetail=eventdetail)
                else:
                    return JsonResponse({'msg': '收藏过多！'})
            else:
                return JsonResponse({'msg': '您已经收藏！'})
        except BaseException:
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})


@method_decorator(customer_login_required, name='dispatch')
class FollowView(View):
    '''
    用户收藏列表信息
    '''

    def get(self, request):
        user = request.user
        objs = user.follow_set.all()
        context = {}
        list = []
        for obj in objs:
            value = [{
                'eventdetail': (obj.eventdetail.building +
                                '-' +
                                obj.eventdetail.unit +
                                '-' +
                                obj.eventdetail.floor +
                                '-' +
                                obj.eventdetail.room_num),
                'price': obj.eventdetail.total,
            }]
            list.append(value)
        context['objects'] = list
        return JsonResponse(context)


@method_decorator(customer_login_time, name='dispatch')
@method_decorator(customer_login_required, name='dispatch')
class AppHouseChoiceConfirmView(View):
    '''
    订单确认
    '''

    def post(self, request):
        user = request.user
        house = request.POST.get('house')
        try:
            eventdetail = EventDetail.get(house)
            if not eventdetail.is_sold:
                if not Order.objects.filter(
                        user=user,
                        eventdetail=eventdetail):
                    if user.order_set.count() < user.customer.count:
                        a = Order.objects.create(
                            user=user,
                            eventdetail=eventdetail,
                            event=eventdetail.event,  # 需要去掉event
                            order_num=time.strftime('%Y%m%d%H%M%S'))
                        if a.time <= a.event.test_end:
                            a.is_test = True
                            a.save()
                        else:
                            a.is_test = False
                            a.save()
                    else:
                        return JsonResponse({'success': False})
                else:
                    return JsonResponse({'success': False})
            else:
                return JsonResponse({'success': False})
        except BaseException:
            return JsonResponse({'success': False})
        else:
            return JsonResponse(
                {
                    'success': True,
                    'room_info': (
                        eventdetail.building +
                        '-' +
                        eventdetail.unit +
                        '-' +
                        eventdetail.floor +
                        '-' +
                        eventdetail.room_num),
                    'limit': eventdetail.event.limit,
                    'ordertime': a.time,
                    'orderid': a.id,
                })


@method_decorator(customer_login_time, name='dispatch')
@method_decorator(customer_login_required, name='dispatch')
class AppOrderListView(View):
    '''
    订单列表
    '''

    def get(self, request):
        user = request.user
        objs = user.order_set.all()
        valuelist = []
        for obj in objs:
            value = [{
                'order_num': obj.order_num,
                'room_info': (
                    obj.eventdetail.building +
                    '-' +
                    obj.eventdetail.unit +
                    '-' +
                    obj.eventdetail.floor +
                    '-' +
                    obj.eventdetail.room_num),
                'time': obj.time,
                'event': obj.eventdetail.event.name,
                'unit_price': obj.eventdetail.unit_price if obj.eventdetail.event.covered_space_price else '',
                'choice_num': '0000000000000001',  # 这里需要确认一下
            }]
            valuelist.append(value)
        context = {}
        context['objects'] = valuelist
        return JsonResponse(context)


@method_decorator(customer_login_time, name='dispatch')
@method_decorator(customer_login_required, name='dispatch')
class AppOrderInfoView(View):
    '''
    订单详情
    '''

    def get(self, request):
        orderid = request.GET.get('orderId')
        try:
            obj = Order.get(orderid)
            value = [{
                'eventname': obj.eventdetail.event.name,
                'unit_price': obj.eventdetail.unit_price,
                'limit': obj.eventdetail.event.limit,
                'ordertime': obj.time.strftime('%Y%m%d %H:%M:%S'),
                'room_info': (
                    obj.eventdetail.building +
                    '-' +
                    obj.eventdetail.unit +
                    '-' +
                    obj.eventdetail.floor +
                    '-' +
                    obj.eventdetail.room_num),
                'houst_type': '三室两厅',  # 这里需要改
                'area': obj.eventdetail.area,
                'customer': obj.user.customer.realname,
                'mobile': obj.user.customer.mobile,
                'iidentication': obj.user.customer.identication,
                'order_num': obj.order_num,
                'orderid': obj.id,
            }]
            context = {}
            context['objects'] = value
            context['success'] = True
        except BaseException:
            return JsonResponse({'success': False})
        else:
            return JsonResponse(context)
