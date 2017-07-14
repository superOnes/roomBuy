from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404

from apt.models import Event, EventDetail


class Customer(models.Model):
    realname = models.CharField('姓名', max_length=10)
    mobile = models.CharField('手机号', max_length=20)
    identication = models.CharField('身份证', max_length=50)
    remark = models.TextField('备注', null=True, blank=True)
    protime = models.DateTimeField('同意协议时间', null=True, blank=True)
    heat = models.IntegerField('访问热度', default=0)
    # testroom = models.ForeignKey(EventDetail)
    count = models.IntegerField('可选套数', default=0)
    event = models.ForeignKey(Event, verbose_name='关联活动')
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


class User(AbstractUser):
    is_delete = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    customer = models.OneToOneField(Customer, null=True, blank=True)

    @classmethod
    def remove(cls, id):
        obj = cls.objects.get(id=id)
        obj.is_delete = True
        obj.save()


class Order(models.Model):
    user = models.ForeignKey(User)
    eventdetail = models.ForeignKey(EventDetail)
    time = models.DateTimeField('订单时间', auto_now_add=True)
    event = models.ForeignKey(Event)
    is_delete = models.BooleanField(default=False)
    is_test = models.BooleanField('是否是公测订单', default=True)

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
