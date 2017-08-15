from django.db import models

class Province(models.Model):
    provinceid = models.CharField('省份id', max_length=100, default=True)
    name = models.CharField(max_length=30)


class City(models.Model):
    cityid = models.CharField('城市id', max_length=100, default=True)
    name = models.CharField(max_length=40)
    province = models.ForeignKey(Province)
