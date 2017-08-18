from django.db import models


class Province(models.Model):
    provinceid = models.CharField('省份id', max_length=100)
    name = models.CharField(max_length=30)

    @classmethod
    def all(cls):
        return cls.objects.all()


class City(models.Model):
    cityid = models.CharField('城市id', max_length=100)
    name = models.CharField(max_length=40)
    province = models.ForeignKey(Province)

    @classmethod
    def get_city_by_province(cls, p):
        return cls.objects.filter(province_id=p)
