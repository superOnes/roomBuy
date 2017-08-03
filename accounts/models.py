from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404

from apt.models import Event, EventDetail, Company


class Customer(models.Model):
    realname = models.CharField('姓名', max_length=10)
    mobile = models.CharField('手机号', max_length=20)
    identication = models.CharField('身份证', max_length=50)
    remark = models.TextField('备注', null=True, blank=True)
    protime = models.DateTimeField('同意协议时间', null=True, blank=True)
    heat = models.IntegerField('访问热度', default=0)
    count = models.IntegerField('可选套数', default=1)
    event = models.ForeignKey(Event, verbose_name='关联活动')
    is_delete = models.BooleanField(default=False)
    session_key = models.CharField(
        'session_key',
        max_length=100,
        null=True,
        blank=True)

    @classmethod
    def get(cls, id):
        return get_object_or_404(cls.objects, id=id)

    @classmethod
    def all(cls):
        return cls.objects.filter(is_delete=0).order_by('-id')

    @classmethod
    def get_by_event(cls, eid, id):
        return cls.objects.filter(event_id=eid,
                                  identication=id).first()


class User(AbstractUser):
    is_delete = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, blank=True)
    house_limit = models.IntegerField('房源数量限制', default=0)
    expire_date = models.DateTimeField('账号过期日期', null=True, blank=True)
    customer = models.OneToOneField(Customer, null=True, blank=True)

    @classmethod
    def remove(cls, id):
        obj = cls.objects.get(id=id)
        obj.is_delete = True
        obj.save()

    @classmethod
    def get(cls, id):
        return get_object_or_404(cls.objects, id=id)

    def get_order_count(self):
        return self.order_set.filter(is_test=False).count()


class Order(models.Model):
    user = models.ForeignKey(User)
    eventdetail = models.ForeignKey(EventDetail)
    time = models.DateTimeField('订单时间', auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_test = models.BooleanField('是否是公测订单', default=True)
    order_num = models.CharField('订单编号', max_length=100)

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
