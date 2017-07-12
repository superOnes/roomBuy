from django.db import models
from django.contrib.auth.models import AbstractUser

from apt.models import Event, EventDetail


class Customer(models.Model):
    realname = models.CharField('姓名', max_length=10)
    mobile = models.CharField('手机号', max_length=20)
    identication = models.CharField('身份证', max_length=50)
    remark = models.TextField('备注', null=True, blank=True)
    count = models.IntegerField(default=0)
    event = models.ForeignKey(Event)


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
    customer = models.ForeignKey(User)
    eventdetail = models.ForeignKey(EventDetail)
    time = models.DateTimeField('公测订单时间')
    opentime = models.DateTimeField('开盘订单时间')
    event = models.ForeignKey(Event)
    is_delete = models.BooleanField(default=False)

    def get(cls, id):
        return cls.objects.filter(id=id).first()

    def all(cls):
        return cls.objects.filter(is_delete=0).order_by('-id')

    def remove(cls, id):
        obj = cls.get(id)
        obj.is_delete = True
        obj.save()