from django.db import models
from accounts.models import User
from apt.models import EventDetail


class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name='顾客')
    eventdetail = models.ForeignKey(EventDetail, verbose_name='房源/车位信息')
