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
    is_pub = models.BooleanField('是否发布', default=False)
    is_delete = models.BooleanField(default=False)

    @classmethod
    def get(cls, id):
        return get_object_or_404(cls.objects, id=id)

    @classmethod
    def all(cls):
        return cls.objects.filter(is_delete=0).order_by('-id')

    @classmethod
    def remove(cls, id):
        obj = cls.get(id)
        obj.is_delete = True
        obj.save()


class HouseType(models.Model):
    name = models.CharField('户型名称', max_length=100)
    pic = models.ImageField('户型照片', upload_to='housetype/%Y/%m/%d/')
    event = models.ForeignKey(Event)
    num = models.IntegerField('编号', null=True, blank=True)

    @classmethod
    def get_obj_by_num(cls, num):
        return cls.objects.filter(num=num).first()


class EventDetail(models.Model):
    building = models.CharField('楼号', max_length=50)
    unit = models.CharField('单元', max_length=100)
    floor = models.CharField('楼层', max_length=100)
    room_num = models.CharField('房号', max_length=50)
    price = models.CharField('原价', max_length=100)
    total = models.CharField('线上总价', max_length=100)
    status = models.BooleanField('上架状态', default=False)
    event = models.ForeignKey(Event, verbose_name='所属活动')
    is_sold = models.BooleanField('是否被卖', default=False)
    is_testsold = models.BooleanField('公测是否已售', default=False)
    remark = models.TextField('描述补充', blank=True)
    image = models.ImageField('图片', upload_to='eventdetail/%Y/%m/%d/',
                              null=True, blank=True)
    num = models.IntegerField('收藏人数', default=0)
    visit_num = models.IntegerField('访问热度', default=0)
    is_delete = models.BooleanField(default=False)
    house_type = models.ForeignKey(HouseType, null=True, blank=True)
    looking=models.CharField('朝向',max_length=100)
    term=models.CharField('使用年限',max_length=50)
    area=models.CharField('建筑面积',max_length=50)
    unit_price=models.CharField('面积单价',max_length=100)

    @classmethod
    def get(cls, id):
        return get_object_or_404(cls.objects, id=id)

    @classmethod
    def all(cls):
        return cls.objects.filter(is_delete=0).order_by('-id')

    @classmethod
    def remove(cls, id):
        obj = cls.get(id)
        obj.is_delete = True
        obj.save()
