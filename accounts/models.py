from django.db import models
from django.contrib.auth.models import AbstractUser

from apt.models import Event


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
