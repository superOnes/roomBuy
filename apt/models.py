from django.db import models
from django.shortcuts import get_object_or_404

class Event(models.Model):
    APT = 1
    PARKING = 2
    TYPES = (
        (APT, '房间开盘'),
        (PARKING, '车位开盘'),
    )
    type = models.PositiveSmallIntegerField('活动类型', choices=TYPES, default=APT)
    name = models.CharField('活动名称', max_length=100)
    phone_num = models.CharField('咨询电话', max_length=50, null=True, blank=True)
    test_start = models.DateTimeField('公测开始时间')
    test_end = models.DateTimeField('公测结束时间')
    test_price = models.BooleanField('是否显示公测放价', default=False)
    event_start = models.DateTimeField('活动开始时间')
    event_end = models.DateTimeField('活动结束时间')
    limit = models.IntegerField('选房完成期限')
    equ_login_num = models.IntegerField('支持设备登录数')
    follow_num = models.IntegerField('同一账号允许收藏数')
    login_msg = models.BooleanField('登录短信提醒', default=False)
    price = models.BooleanField('是否显示原价', default=False)
    covered_space = models.BooleanField('是否显示建筑面积', default=False)
    covered_space_price = models.BooleanField('是否显示建筑面积单价', default=False)
    inside_space = models.BooleanField('是否显示套内面积', default=False)
    inside_space_price = models.BooleanField('是否显示套内面积单价', default=False)
    description = models.TextField('活动细则')
    notice = models.TextField('认购须知')
    tip = models.TextField('温馨提示')
    cover = models.ImageField('活动封面', upload_to='cover/%Y/%m/%d/',
                              null=True, blank=True)
    plane_graph = models.ImageField('平面图', upload_to='planeGraph/%Y/%m/%d/',
                                    null=True, blank=True)
    termname = models.CharField('协议名称', max_length=100, null=True, blank=True)
    term = models.TextField('协议内容', null=True, blank=True)

    @classmethod
    def get(cls, id):
        return get_object_or_404(cls.objects, id=id)


class EventDetail(models.Model):
    # batch = models.CharField('期/批', max_length=50)
    building = models.CharField('楼号', max_length=50)
    unit = models.CharField('单元', max_length=100)
    floor = models.IntegerField('楼层', max_length=50)
    room_num = models.CharField('房号', max_length=50)
    price = models.CharField('原价', max_length=100)
    total = models.CharField('线上总价', max_length=100)
    status = models.BooleanField('上架状态', default=False)
    event = models.ForeignKey(Event, verbose_name='所属活动')
    # house_type = models.CharField('户型', max_length=100)
    # floor_area = models.CharField('建筑面积', max_length=50)
    is_sold = models.BooleanField('是否被卖', default=False)
    remark = models.TextField('描述补充', blank=True)
    image = models.ImageField('平面图', upload_to='eventdetail/%Y/%m/%d/',
                              null=True, blank=True)
