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

        #内蒙古
        p3 = Province.objects.get(provinceid='150000')
        if p3:
            City.objects.create(cityid='150100', name='呼和浩特市', province=p3)
            City.objects.create(cityid='150200', name='包头市', province=p3)
            City.objects.create(cityid='150300', name='乌海市', province=p3)
            City.objects.create(cityid='150400', name='赤峰市', province=p3)
            City.objects.create(cityid='150500', name='通辽市', province=p3)
            City.objects.create(cityid='150600', name='鄂尔多斯市', province=p3)
            City.objects.create(cityid='150700', name='呼伦贝尔市', province=p3)
            City.objects.create(cityid='150800', name='巴彦卓尔市', province=p3)
            City.objects.create(cityid='150900', name='乌兰察布市', province=p3)
            City.objects.create(cityid='151000', name='兴安盟', province=p3)
            City.objects.create(cityid='151100', name='锡林郭勒盟', province=p3)
            City.objects.create(cityid='151200', name='阿拉善盟', province=p3)

        #辽宁省
        p4 = Province.objects.get(provinceid='210000')
        if p4:
            City.objects.create(cityid='210100', name='沈阳市', province=p4)
            City.objects.create(cityid='210200', name='大连市', province=p4)
            City.objects.create(cityid='210300', name='鞍山市', province=p4)
            City.objects.create(cityid='210400', name='抚顺市', province=p4)
            City.objects.create(cityid='210500', name='本溪市', province=p4)
            City.objects.create(cityid='210600', name='丹东市', province=p4)
            City.objects.create(cityid='210700', name='锦州市', province=p4)
            City.objects.create(cityid='210800', name='营口市', province=p4)
            City.objects.create(cityid='210900', name='阜新市', province=p4)
            City.objects.create(cityid='211000', name='辽阳市', province=p4)
            City.objects.create(cityid='211100', name='盘锦市', province=p4)
            City.objects.create(cityid='211200', name='铁岭市', province=p4)
            City.objects.create(cityid='211300', name='朝阳市', province=p4)
            City.objects.create(cityid='211400', name='葫芦岛市', province=p4)

        #吉林市
        p5 = Province.objects.get(provinceid='220000')
        if p5:
            City.objects.create(cityid='220100', name='长春市', province=p5)
            City.objects.create(cityid='220200', name='吉林市', province=p5)
            City.objects.create(cityid='220300', name='四平市', province=p5)
            City.objects.create(cityid='220400', name='辽源市', province=p5)
            City.objects.create(cityid='220500', name='通化市', province=p5)
            City.objects.create(cityid='220600', name='白山市', province=p5)
            City.objects.create(cityid='220700', name='松原市', province=p5)
            City.objects.create(cityid='220800', name='白城市', province=p5)
            City.objects.create(cityid='222400', name='延边朝鲜自治州', province=p5)

        #黑龙江市
        p6 = Province.objects.get(provinceid='230000')
        if p6:
            City.objects.create(cityid='230100', name='哈尔滨市', province=p6)
            City.objects.create(cityid='230200', name='齐齐哈尔市', province=p6)
            City.objects.create(cityid='230300', name='鸡西市', province=p6)
            City.objects.create(cityid='230400', name='鹤岗市', province=p6)
            City.objects.create(cityid='230500', name='双鸭山市', province=p6)
            City.objects.create(cityid='230600', name='大庆市', province=p6)
            City.objects.create(cityid='230700', name='伊春市', province=p6)
            City.objects.create(cityid='230800', name='佳木斯市', province=p6)
            City.objects.create(cityid='230900', name='七台河市', province=p6)
            City.objects.create(cityid='231000', name='牡丹江市', province=p6)
            City.objects.create(cityid='231100', name='黑河市', province=p6)
            City.objects.create(cityid='231200', name='绥化市', province=p6)
            City.objects.create(cityid='232700', name='大兴安岭地区', province=p6)

        # 江苏省
        p7 = Province.objects.get(provinceid='320000')
        # 浙江省
        p7 = Province.objects.get(provinceid='330000')
        # 安徽省
        p7 = Province.objects.get(provinceid='340000')
        # 福建省
        p7 = Province.objects.get(provinceid='350000')
        # 江西省
        p7 = Province.objects.get(provinceid='360000')
        # 山东省
        p7 = Province.objects.get(provinceid='370000')
        # 河南省
        p7 = Province.objects.get(provinceid='410000')
        # 湖北省
        p7 = Province.objects.get(provinceid='420000')
        # 湖南省
        p7 = Province.objects.get(provinceid='430000')
        # 广东省
        p7 = Province.objects.get(provinceid='320000')
        # 广西壮族自治区
        p7 = Province.objects.get(provinceid='450000')
        # 海南省
        p7 = Province.objects.get(provinceid='460000')
        # 四川省
        p7 = Province.objects.get(provinceid='510000')
        # 贵州省
        p7 = Province.objects.get(provinceid='520000')
        # 云南省
        p7 = Province.objects.get(provinceid='530000')
        # 西藏
        p7 = Province.objects.get(provinceid='540000')
        # 陕西省
        p7 = Province.objects.get(provinceid='610000')
        # 甘肃省
        p7 = Province.objects.get(provinceid='620000')
        # 青海省
        p7 = Province.objects.get(provinceid='630000')
        # 宁夏回族自治区
        p7 = Province.objects.get(provinceid='640000')
        # 新疆
        p7 = Province.objects.get(provinceid='650000')
        # 香港
        # 澳门
        # 台湾











