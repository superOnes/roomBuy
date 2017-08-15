from django.core.management import BaseCommand

from backstage.models import Province, City


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Province.objects.all().delete()
        Province.objects.create(provinceid='110000', name='北京')
        Province.objects.create(provinceid='120000', name='天津市')
        Province.objects.create(provinceid='310000', name='上海市')
        Province.objects.create(provinceid='500000', name='重庆市')
        Province.objects.create(provinceid='130000', name='河北省')
        Province.objects.create(provinceid='140000', name='山西省')
        Province.objects.create(provinceid='150000', name='内蒙古')
        Province.objects.create(provinceid='210000', name='辽宁省')
        Province.objects.create(provinceid='220000', name='吉林省')
        Province.objects.create(provinceid='230000', name='黑龙江省')
        Province.objects.create(provinceid='320000', name='江苏省')
        Province.objects.create(provinceid='330000', name='浙江省')
        Province.objects.create(provinceid='340000', name='安徽省')
        Province.objects.create(provinceid='350000', name='福建省')
        Province.objects.create(provinceid='360000', name='江西省')
        Province.objects.create(provinceid='370000', name='山东省')
        Province.objects.create(provinceid='410000', name='河南省')
        Province.objects.create(provinceid='420000', name='湖北省')
        Province.objects.create(provinceid='430000', name='湖南省')
        Province.objects.create(provinceid='440000', name='广东省')
        Province.objects.create(provinceid='450000', name='广西壮族自治区')
        Province.objects.create(provinceid='460000', name='海南省')
        Province.objects.create(provinceid='510000', name='四川省')
        Province.objects.create(provinceid='520000', name='贵州省')
        Province.objects.create(provinceid='530000', name='云南省')
        Province.objects.create(provinceid='540000', name='西藏')
        Province.objects.create(provinceid='610000', name='陕西省')
        Province.objects.create(provinceid='620000', name='甘肃省')
        Province.objects.create(provinceid='630000', name='青海省')
        Province.objects.create(provinceid='640000', name='宁夏')
        Province.objects.create(provinceid='650000', name='新疆')
        Province.objects.create(provinceid='810000', name='香港')
        Province.objects.create(provinceid='820000', name='澳门')
        Province.objects.create(provinceid='710000', name='台湾')

        City.objects.all().delete()
        # 河北
        p1 = Province.objects.get(provinceid='130000')
        if p1:
            City.objects.create(cityid='130100', name='石家庄市', province=p1)
            City.objects.create(cityid='130200', name='唐山市', province=p1)
            City.objects.create(cityid='130300', name='秦皇岛市', province=p1)
            City.objects.create(cityid='130400', name='邯郸市', province=p1)
            City.objects.create(cityid='130500', name='邢台市', province=p1)
            City.objects.create(cityid='130600', name='保定市', province=p1)
            City.objects.create(cityid='130700', name='张家口市', province=p1)
            City.objects.create(cityid='130800', name='承德市', province=p1)
            City.objects.create(cityid='130900', name='沧州市', province=p1)
            City.objects.create(cityid='131000', name='廊坊市', province=p1)
            City.objects.create(cityid='131100', name='衡水市', province=p1)

        # 山西
        p2 = Province.objects.get(provinceid='140000')
        if p2:
            City.objects.create(cityid='140100', name='太原市', province=p2)
            City.objects.create(cityid='140200', name='大同市', province=p2)
            City.objects.create(cityid='140300', name='阳泉市', province=p2)
            City.objects.create(cityid='140400', name='长治市', province=p2)
            City.objects.create(cityid='140500', name='晋城市', province=p2)
            City.objects.create(cityid='140600', name='朔州市', province=p2)
            City.objects.create(cityid='140700', name='晋中市', province=p2)
            City.objects.create(cityid='140800', name='运城市', province=p2)
            City.objects.create(cityid='140900', name='忻州市', province=p2)
            City.objects.create(cityid='141000', name='临汾市', province=p2)
            City.objects.create(cityid='141100', name='吕梁市', province=p2)







