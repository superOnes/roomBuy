import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse

from apt.models import Event, EventDetail
from aptp.models import Follow
from accounts.models import Customer


class AppEventDetailView(View):
    '''
    显示活动
    '''

    def get(self, request, pk):
        obj = Event.get(pk)
        if obj:
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
        return JsonResponse({'success': False})


class AppEventDetailListView(View):
    '''
    车位/房源 楼号列表
    '''

    def get(self, request, pk):
        eventobj = Event.get(pk)
        context = {}
        eventdetobj = EventDetail.objects.filter(event_id=pk)
        if eventobj:
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
        return JsonResponse({'success': False})


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
        if eventdetobj:
            unitlist = []
            for obj in eventdetobj:
                unitlist.append((obj.unit))
            value = [{
                'unit': list(set(unitlist))
            }]
            context['objects'] = value
            return JsonResponse(context)
        return JsonResponse({'success': False})


class AppEventDetailRoomListView(View):
    '''
    车位/房源 房号列表
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        building = request.GET.get('building')
        unit = request.GET.get('unit')
        context = {}
        eventdetobj = EventDetail.objects.filter(
            building=building, unit=unit, event_id=eventid)
        if eventdetobj:
            room_num_list=[]
            for obj in eventdetobj:
                value = [{
                    'floor': obj.floor,
                    'room_num': obj.room_num,
                    'is_sold': obj.is_sold,
                }]
                room_num_list.append(value)
            context['objects'] = room_num_list
            return JsonResponse(context)
        return JsonResponse({'success': False})


class FollowView(View):
    '''
    用户收藏信息
    '''

    def get(self, request, **kwargs):
        user = request.user
        objs = Follow.objects.filter(user=user)
        context = {}
        if objs:
            list = []
            for obj in objs:
                value = [{
                    'eventdetail': (obj.eventdetail.building +
                                    '楼' +
                                    obj.eventdetail.unit +
                                    '单元' +
                                    obj.eventdetail.floor +
                                    '层' +
                                    obj.eventdetail.room_num + '号'),
                    'price': obj.eventdetail.price,
                }]
                list.append(value)
            context['objects'] = list
            return JsonResponse(context)
        return JsonResponse({'success': False})


class AppEventDetailDetailView(View):
    '''
    车位/房源 详情
    '''

    def get(self, request, pk):
        obj = EventDetail.get(pk)
        if obj:
            value = [{

            }]
            context = {}
            context['objects'] = value
            return JsonResponse(context)
        return JsonResponse({'success': False})


class AppHouseSuccessView(TemplateView):
    template_name = 'aptp/house_success.html'


class AppOrderListView(TemplateView):
    template_name = 'aptp/order_list.html'


class AppOrderInfoView(TemplateView):
    template_name = 'aptp/order_info.html'
