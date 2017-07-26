import time
from datetime import datetime, timedelta

from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import connection, transaction

from apt.models import Event, EventDetail
from aptp.models import Follow
from accounts.models import Order, Customer, User
from accounts.decorators import customer_login_required, customer_login_time


class ProView(View):
    '''
    显示协议
    '''

    def get(self, request):
        mobile = request.GET.get('tel')
        identication = request.GET.get('personId')
        try:
            customer = Customer.objects.get(
                mobile=mobile, identication=identication)
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '认筹名单中没有该用户！'})
        else:
            value = [{
                'termname': customer.event.termname,
                'term': customer.event.term,
                'userid': customer.user.id,
            }]
            context = {}
            context['objects'] = value
            context['response_state'] = 200
            return JsonResponse(context)


# @method_decorator(customer_login_required, name='dispatch')
class AppEventDetailView(View):
    '''
    显示活动
    '''

    def get(self, request, pk):
        obj = Event.get(pk)
        value = [
            {
                'test_start': (
                    obj.test_start).strftime("%Y/%m/%d %H:%M:%S"),
                'test_ent': (
                    obj.test_end).strftime("%Y/%m/%d %H:%M:%S"),
                'event_start': (
                    obj.event_start).strftime("%Y/%m/%d %H:%M:%S"),
                'event_end': (
                        obj.event_end).strftime("%Y/%m/%d %H:%M:%S"),
                'notice': obj.notice,
                'description': obj.description,
                'tip': obj.tip,
                'name': obj.name,
                'plane_graph': obj.plane_graph.url,
                'phone': obj.phone_num,
            }]
        context = {}
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)

# @method_decorator(customer_login_required, name='dispatch')


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
            'building': sorted(list(set(buildinglist))),
        }]
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)


# @method_decorator(customer_login_required, name='dispatch')
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
            'unit': sorted(list(set(unitlist)))
        }]
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)


# @method_decorator(customer_login_required, name='dispatch')
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
            if obj.status:
                value = [{
                    'house': obj.id,
                    'floor_room_num': str(obj.floor) + '-' + str(obj.room_num),
                    'is_sold': obj.is_sold,
                }]
                room_num_list.append(value)
        context['objects'] = room_num_list
        context['response_state'] = 200
        return JsonResponse(context)


# @method_decorator(customer_login_time, name='dispatch')
# @method_decorator(customer_login_required, name='dispatch')
class AppEventDetailHouseInfoView(View):
    '''
    车位/房源 详情
    '''

    def get(self, request):
        userid = request.GET.get('userid')
        user = User.get(userid)
        house = request.GET.get('house')
        eventdetobj = EventDetail.get(house)
        eventdetobj.visit_num = eventdetobj.visit_num + 1
        eventdetobj.save()
        test = True if time.strftime('%Y%m%d %H:%M:%S') <= eventdetobj.event.test_end.strftime(
            '%Y%m%d %H:%M:%S') else False
        try:
            Follow.objects.get(user=request.user, eventdetail=eventdetobj)
        except BaseException:
            is_followed = False,
        else:
            is_followed = True,
        value = [{'event': user.customer.event.name,
                  'realname': user.customer.realname,
                  'mobile': user.customer.mobile,
                  'identication': user.customer.identication,
                  'building_unit': eventdetobj.building + eventdetobj.unit + str(eventdetobj.floor) + '层 ' + str(eventdetobj.room_num) + '室',
                  'total': '***' if test and not eventdetobj.event.test_price else ((eventdetobj.area) * (eventdetobj.unit_price)),
                  'house_type': eventdetobj.house_type.name,
                  'pic': eventdetobj.house_type.pic.url,
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
        context['response_state'] = 200
        return JsonResponse(context)

# @method_decorator(customer_login_required, name='dispatch')


class AddFollow(View):
    '''
    添加收藏
    '''

    def post(self, request):
        house = request.POST.get('house')
        userid = request.POST.get('userid')
        user = User.get(userid)
        try:
            eventdetail = EventDetail.get(house)
            if not Follow.objects.filter(
                    user=user,
                    eventdetail=eventdetail):
                if user.follow_set.count() < user.customer.event.follow_num:
                    Follow.objects.create(
                        user=user, eventdetail=eventdetail)
                else:
                    return JsonResponse(
                        {'response_state': 403, 'msg': '收藏数量超过限制'})
            else:
                return JsonResponse(
                    {'response_state': 400, 'msg': '您已收藏过该商品！'})
        except BaseException:
            return JsonResponse({'response_state': 400})
        else:
            return JsonResponse({'response_state': 200, 'msg': '收藏成功'})


# @method_decorator(customer_login_required, name='dispatch')
class FollowView(View):
    '''
    用户收藏列表信息
    '''

    def get(self, request):
        userid = request.GET.get('userid')
        user = User.get(userid)
        objs = user.follow_set.all()
        context = {}
        list = []
        for obj in objs:
            value = [
                {
                    'eventdetail': (
                        obj.eventdetail.building +
                        obj.eventdetail.unit +
                        str(obj.eventdetail.floor) +
                        '层' +
                        str(obj.eventdetail.room_num)) + '室',
                    'price': (
                        (
                            obj.eventdetail.area) *
                        (
                            obj.eventdetail.unit_price)),
                    'house': obj.eventdetail.id,
                }]
            list.append(value)
        context['objects'] = list
        context['response_state'] = 200
        return JsonResponse(context)


# @method_decorator(customer_login_time, name='dispatch')
# @method_decorator(customer_login_required, name='dispatch')
class AppHouseChoiceConfirmView(View):
    '''
    订单确认
    '''

    def post(self, request):
        house = request.POST.get('house')
        userid = request.POST.get('userid')
        user = User.get(userid)
        cursor = connection.cursor()
        # cursor.execute('SELECT id,is_sold,sign_id,event_id,is_testsold,\
        #                 building,unit,floor,room_num FROM apt_eventdetail \
        #                 where id=%s FOR UPDATE' % house)
        cursor.execute('SELECT id,is_sold,sign_id,event_id,is_testsold,\
                        building,unit,floor,room_num FROM apt_eventdetail \
                        where id=%s' % house)
        obj = cursor.fetchone()
        if obj is None:
            return JsonResponse({'response_state': 404, 'msg': '目标不存在'})
        event = Event.get(obj[3])
        now = datetime.now()
        if (now >= event.test_start) and (now <= event.test_end):
            if not obj[4]:
                with transaction.atomic():
                    order = Order.objects.create(user=user,
                                                 eventdetail_id=obj[0],
                                                 order_num=time.strftime
                                                 ('%Y%m%d%H%M%S'))
                    cursor.execute('UPDATE apt_eventdetail set is_testsold=1 \
                                    where id=%s' % house)
                return JsonResponse({'response_state': 200,
                                     'room_info': ('%s-%s-%s-%s') %
                                                  (obj[5], obj[6], obj[7],
                                                   obj[8]),
                                     'limit': event.limit,
                                     'ordertime': order.time,
                                     'orderid': order.id,
                                     })
        elif (now >= event.event_start) and (now <= event.event_end):
            if not obj[1] and not obj[2]:
                with transaction.atomic():
                    order = Order.objects.create(user=user,
                                                 eventdetail_id=obj[0],
                                                 order_num=time.strftime
                                                 ('%Y%m%d%H%M%S'),
                                                 is_test=False)
                    cursor.execute('UPDATE apt_eventdetail set is_sold=1 \
                                    where id=%s' % house)
                return JsonResponse({'response_state': 200,
                                     'room_info': ('%s-%s-%s-%s') %
                                     (obj[5], obj[6], obj[7],
                                      obj[8]),
                                     'limit': event.limit,
                                     'ordertime': order.time,
                                     'orderid': order.id,
                                     })
            elif obj[2]:
                with transaction.atomic():
                    customer = Customer.get(obj[2])
                    Order.objects.create(user_id=customer.user.id,
                                         eventdetail_id=obj[0],
                                         order_num=time.strftime
                                         ('%Y%m%d%H%M%S'),
                                         is_test=False)
                    cursor.execute(
                        'UPDATE apt_eventdetail set is_sold=1 where id=%s' %
                        house)
                return JsonResponse(
                    {'response_state': 400, 'msg': '购买失败，房屋已卖出'})
        return JsonResponse({'response_state': 400, 'msg': '购买失败'})


class OrderProView(View):
    '''
    订单中协议
    '''

    def get(self, request):
        userid = request.GET.get('userid')
        try:
            customer = User.get(userid).customer
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '认筹名单中没有该用户！'})
        else:
            value = [{
                'termname': customer.event.termname,
                'term': customer.event.term,
            }]
            context = {}
            context['objects'] = value
            context['response_state'] = 200
            return JsonResponse(context)

# @method_decorator(customer_login_time, name='dispatch')
# @method_decorator(customer_login_required, name='dispatch')


class AppOrderListView(View):
    '''
    订单列表
    '''

    def get(self, request):
        userid = request.GET.get('userid')
        user = User.get(userid)
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
                    str(obj.eventdetail.floor) +
                    '-' +
                    str(obj.eventdetail.room_num)),
                'time': obj.time.strftime('%Y/%m/%d %H:%M:%S'),
                'event': obj.eventdetail.event.name,
                'unit_price': obj.eventdetail.unit_price if obj.eventdetail.event.covered_space_price else '',
                'orderid': obj.id,
            }]
            valuelist.append(value)
        context = {}
        context['objects'] = valuelist
        context['response_state'] = 200
        return JsonResponse(context)


# @method_decorator(customer_login_time, name='dispatch')
# @method_decorator(customer_login_required, name='dispatch')
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
                'limit': (obj.time + timedelta(hours=obj.eventdetail.event.limit)).strftime('%Y年%m月%d日 %H:%M:%S'),
                'ordertime': obj.time.strftime('%Y%m/%d %H:%M:%S'),
                'room_info': (
                    obj.eventdetail.event.name +
                    '-' +
                    obj.eventdetail.building +
                    '-' +
                    obj.eventdetail.unit +
                    '-' +
                    str(obj.eventdetail.floor) +
                    '-' +
                    str(obj.eventdetail.room_num)),
                'houst_type': obj.eventdetail.house_type.name,
                'area': obj.eventdetail.area,
                'customer': obj.user.customer.realname,
                'mobile': obj.user.customer.mobile,
                'iidentication': obj.user.customer.identication,
                'order_num': obj.order_num,
                'total':((obj.eventdetail.area) * (obj.eventdetail.unit_price))
            }]

            context = {}
            context['objects'] = value
            context['response_state'] = 200
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '没有找到该订单！'})
        else:
            return JsonResponse(context)
