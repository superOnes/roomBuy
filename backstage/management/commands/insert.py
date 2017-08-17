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
        P7 = Province.objects.get(provinceid='320000')
        if P7:
            City.objects.create(cityid=320100, name='南京市', province=P7)
            City.objects.create(cityid=320200, name='无锡市', province=P7)
            City.objects.create(cityid=320300, name='徐州市', province=P7)
            City.objects.create(cityid=320400, name='常州市', province=P7)
            City.objects.create(cityid=320500, name='苏州市', province=P7)
            City.objects.create(cityid=320600, name='南通市', province=P7)
            City.objects.create(cityid=320700, name='连云港市', province=P7)
            City.objects.create(cityid=320800, name='淮安市', province=P7)
            City.objects.create(cityid=320900, name='盐城市', province=P7)
            City.objects.create(cityid=321000, name='扬州市', province=P7)
            City.objects.create(cityid=321100, name='镇江市', province=P7)
            City.objects.create(cityid=321200, name='泰州市', province=P7)
            City.objects.create(cityid=321300, name='宿迁市', province=P7)

        # 浙江省
        P8 = Province.objects.get(provinceid='330000')
        if P8:
            City.objects.create(cityid=330100, name='杭州市', province=P8)
            City.objects.create(cityid=330200, name='宁波市', province=P8)
            City.objects.create(cityid=330300, name='温州市', province=P8)
            City.objects.create(cityid=330400, name='嘉兴市', province=P8)
            City.objects.create(cityid=330500, name='湖州市', province=P8)
            City.objects.create(cityid=330600, name='绍兴市', province=P8)
            City.objects.create(cityid=330700, name='金华市', province=P8)
            City.objects.create(cityid=330800, name='衢州市', province=P8)
            City.objects.create(cityid=330900, name='舟山市', province=P8)
            City.objects.create(cityid=331000, name='台州市', province=P8)
            City.objects.create(cityid=331100, name='丽水市', province=P8)

        # 安徽省
        P9 = Province.objects.get(provinceid='340000')
        if P9:
            City.objects.create(cityid=340100, name='合肥市', province=P9)
            City.objects.create(cityid=340200, name='芜湖市', province=P9)
            City.objects.create(cityid=340300, name='蚌埠市', province=P9)
            City.objects.create(cityid=340400, name='淮南市', province=P9)
            City.objects.create(cityid=340500, name='马鞍山市', province=P9)
            City.objects.create(cityid=340600, name='淮北市', province=P9)
            City.objects.create(cityid=340700, name='铜陵市', province=P9)
            City.objects.create(cityid=340800, name='安庆市', province=P9)
            City.objects.create(cityid=341000, name='黄山市', province=P9)
            City.objects.create(cityid=341100, name='滁州市', province=P9)
            City.objects.create(cityid=341200, name='阜阳市', province=P9)
            City.objects.create(cityid=341300, name='宿州市', province=P9)
            City.objects.create(cityid=341500, name='六安市', province=P9)
            City.objects.create(cityid=341600, name='亳州市', province=P9)
            City.objects.create(cityid=341700, name='池州市', province=P9)
            City.objects.create(cityid=341800, name='宣城市', province=P9)
        # 福建省
        P10 = Province.objects.get(provinceid='350000')
        if P10:
            City.objects.create(cityid=350300, name='莆田市', province=P10)
            City.objects.create(cityid=350400, name='三明市', province=P10)
            City.objects.create(cityid=350500, name='泉州市', province=P10)
            City.objects.create(cityid=350600, name='漳州市', province=P10)
            City.objects.create(cityid=350700, name='南平市', province=P10)
            City.objects.create(cityid=350800, name='龙岩市', province=P10)
            City.objects.create(cityid=350900, name='宁德市', province=P10)

        # 江西省
        P11 = Province.objects.get(provinceid='360000')
        if P11:
            City.objects.create(cityid=360100, name='南昌市', province=P11)
            City.objects.create(cityid=360200, name='景德镇市', province=P11)
            City.objects.create(cityid=360300, name='萍乡市', province=P11)
            City.objects.create(cityid=360400, name='九江市', province=P11)
            City.objects.create(cityid=360500, name='新余市', province=P11)
            City.objects.create(cityid=360600, name='鹰潭市', province=P11)
            City.objects.create(cityid=360700, name='赣州市', province=P11)
            City.objects.create(cityid=360800, name='吉安市', province=P11)
            City.objects.create(cityid=360900, name='宜春市', province=P11)
            City.objects.create(cityid=361000, name='抚州市', province=P11)
            City.objects.create(cityid=361100, name='上饶市', province=P11)

        # 山东省
        P12 = Province.objects.get(provinceid='370000')
        if P12:
            City.objects.create(cityid=370100, name='济南市', province=P12)
            City.objects.create(cityid=370200, name='青岛市', province=P12)
            City.objects.create(cityid=370300, name='淄博市', province=P12)
            City.objects.create(cityid=370400, name='枣庄市', province=P12)
            City.objects.create(cityid=370500, name='东营市', province=P12)
            City.objects.create(cityid=370600, name='烟台市', province=P12)
            City.objects.create(cityid=370700, name='潍坊市', province=P12)
            City.objects.create(cityid=370800, name='济宁市', province=P12)
            City.objects.create(cityid=370900, name='泰安市', province=P12)
            City.objects.create(cityid=371000, name='威海市', province=P12)
            City.objects.create(cityid=371100, name='日照市', province=P12)
            City.objects.create(cityid=371200, name='莱芜市', province=P12)
            City.objects.create(cityid=371300, name='临沂市', province=P12)
            City.objects.create(cityid=371400, name='德州市', province=P12)
            City.objects.create(cityid=371500, name='聊城市', province=P12)
            City.objects.create(cityid=371600, name='滨州市', province=P12)
            City.objects.create(cityid=371700, name='菏泽市', province=P12)

        # 河南省
        P13 = Province.objects.get(provinceid='410000')
        if P13:
            City.objects.create(cityid=410100, name='郑州市', province=P13)
            City.objects.create(cityid=410200, name='开封市', province=P13)
            City.objects.create(cityid=410300, name='洛阳市', province=P13)
            City.objects.create(cityid=410400, name='平顶山市', province=P13)
            City.objects.create(cityid=410500, name='安阳市', province=P13)
            City.objects.create(cityid=410600, name='鹤壁市', province=P13)
            City.objects.create(cityid=410700, name='新乡市', province=P13)
            City.objects.create(cityid=410800, name='焦作市', province=P13)
            City.objects.create(cityid=410900, name='濮阳市', province=P13)
            City.objects.create(cityid=411000, name='许昌市', province=P13)
            City.objects.create(cityid=411100, name='漯河市', province=P13)
            City.objects.create(cityid=411200, name='三门峡市', province=P13)
            City.objects.create(cityid=411300, name='南阳市', province=P13)
            City.objects.create(cityid=411400, name='商丘市', province=P13)
            City.objects.create(cityid=411500, name='信阳市', province=P13)
            City.objects.create(cityid=411600, name='周口市', province=P13)
            City.objects.create(cityid=411700, name='驻马店市', province=P13)
            City.objects.create(cityid=419000, name='省直辖县级行政区划', province=P13)

        # 湖北省
        P14= Province.objects.get(provinceid='420000')
        if P14:
            City.objects.create(cityid=420100, name='武汉市', province=P14)
            City.objects.create(cityid=420200, name='黄石市', province=P14)
            City.objects.create(cityid=420300, name='十堰市', province=P14)
            City.objects.create(cityid=420500, name='宜昌市', province=P14)
            City.objects.create(cityid=420600, name='襄阳市', province=P14)
            City.objects.create(cityid=420700, name='鄂州市', province=P14)
            City.objects.create(cityid=420800, name='荆门市', province=P14)
            City.objects.create(cityid=420900, name='孝感市', province=P14)
            City.objects.create(cityid=421000, name='荆州市', province=P14)
            City.objects.create(cityid=421100, name='黄冈市', province=P14)
            City.objects.create(cityid=421200, name='咸宁市', province=P14)
            City.objects.create(cityid=421300, name='随州市', province=P14)
            City.objects.create(cityid=422800, name='恩施土家族苗族自治州', province=P14)
            City.objects.create(cityid=429000, name='省直辖县级行政区划', province=P14)

        # 湖南省
        P15 = Province.objects.get(provinceid='430000')
        if P15:
            City.objects.create(cityid=430100, name='长沙市', province=P15)
            City.objects.create(cityid=430200, name='株洲市', province=P15)
            City.objects.create(cityid=430300, name='湘潭市', province=P15)
            City.objects.create(cityid=430400, name='衡阳市', province=P15)
            City.objects.create(cityid=430500, name='邵阳市', province=P15)
            City.objects.create(cityid=430600, name='岳阳市', province=P15)
            City.objects.create(cityid=430700, name='常德市', province=P15)
            City.objects.create(cityid=430800, name='张家界市', province=P15)
            City.objects.create(cityid=430900, name='益阳市', province=P15)
            City.objects.create(cityid=431000, name='郴州市', province=P15)
            City.objects.create(cityid=431100, name='永州市', province=P15)
            City.objects.create(cityid=431200, name='怀化市', province=P15)
            City.objects.create(cityid=431300, name='娄底市', province=P15)
            City.objects.create(cityid=433100, name='湘西土家族苗族自治州', province=P15)

        # 广东省
        P16 = Province.objects.get(provinceid='320000')
        if P16:
            City.objects.create(cityid=440100, name='广州市', province=P16)
            City.objects.create(cityid=440200, name='韶关市', province=P16)
            City.objects.create(cityid=440300, name='深圳市', province=P16)
            City.objects.create(cityid=440400, name='珠海市', province=P16)
            City.objects.create(cityid=440500, name='汕头市', province=P16)
            City.objects.create(cityid=440600, name='佛山市', province=P16)
            City.objects.create(cityid=440700, name='江门市', province=P16)
            City.objects.create(cityid=440800, name='湛江市', province=P16)
            City.objects.create(cityid=440900, name='茂名市', province=P16)
            City.objects.create(cityid=441200, name='肇庆市', province=P16)
            City.objects.create(cityid=441300, name='惠州市', province=P16)
            City.objects.create(cityid=441400, name='梅州市', province=P16)
            City.objects.create(cityid=441500, name='汕尾市', province=P16)
            City.objects.create(cityid=441600, name='河源市', province=P16)
            City.objects.create(cityid=441700, name='阳江市', province=P16)
            City.objects.create(cityid=441800, name='清远市', province=P16)
            City.objects.create(cityid=441900, name='东莞市', province=P16)
            City.objects.create(cityid=442000, name='中山市', province=P16)
            City.objects.create(cityid=445100, name='潮州市', province=P16)
            City.objects.create(cityid=445200, name='揭阳市', province=P16)
            City.objects.create(cityid=445300, name='云浮市', province=P16)

        # 广西壮族自治区
        P17 = Province.objects.get(provinceid='450000')
        if P17:
            City.objects.create(cityid=450100, name='南宁市', province=P17)
            City.objects.create(cityid=450200, name='柳州市', province=P17)
            City.objects.create(cityid=450300, name='桂林市', province=P17)
            City.objects.create(cityid=450400, name='梧州市', province=P17)
            City.objects.create(cityid=450500, name='北海市', province=P17)
            City.objects.create(cityid=450600, name='防城港市', province=P17)
            City.objects.create(cityid=450700, name='钦州市', province=P17)
            City.objects.create(cityid=450800, name='贵港市', province=P17)
            City.objects.create(cityid=450900, name='玉林市', province=P17)
            City.objects.create(cityid=451000, name='百色市', province=P17)
            City.objects.create(cityid=451100, name='贺州市', province=P17)
            City.objects.create(cityid=451200, name='河池市', province=P17)
            City.objects.create(cityid=451300, name='来宾市', province=P17)
            City.objects.create(cityid=451400, name='崇左市', province=P17)

        # 海南省
        P18 = Province.objects.get(provinceid='460000')
        if P18:
            City.objects.create(cityid=460100, name='海口市', province=P18)
            City.objects.create(cityid=460200, name='三亚市', province=P18)
            City.objects.create(cityid=460300, name='三沙市', province=P18)
            City.objects.create(cityid=460400, name='儋州市', province=P18)
            City.objects.create(cityid=469000, name='省直辖县级行政区划', province=P18)

        # 四川省
        P19 = Province.objects.get(provinceid='510000')
        if P19:
            City.objects.create(cityid=510100, name='成都市', province=P19)
            City.objects.create(cityid=510300, name='自贡市', province=P19)
            City.objects.create(cityid=510400, name='攀枝花市', province=P19)
            City.objects.create(cityid=510500, name='泸州市', province=P19)
            City.objects.create(cityid=510600, name='德阳市', province=P19)
            City.objects.create(cityid=510700, name='绵阳市', province=P19)
            City.objects.create(cityid=510800, name='广元市', province=P19)
            City.objects.create(cityid=510900, name='遂宁市', province=P19)
            City.objects.create(cityid=511000, name='内江市', province=P19)
            City.objects.create(cityid=511100, name='乐山市', province=P19)
            City.objects.create(cityid=511300, name='南充市', province=P19)
            City.objects.create(cityid=511400, name='眉山市', province=P19)
            City.objects.create(cityid=511500, name='宜宾市', province=P19)
            City.objects.create(cityid=511600, name='广安市', province=P19)
            City.objects.create(cityid=511700, name='达州市', province=P19)
            City.objects.create(cityid=511800, name='雅安市', province=P19)
            City.objects.create(cityid=511900, name='巴中市', province=P19)
            City.objects.create(cityid=512000, name='资阳市', province=P19)
            City.objects.create(cityid=513200, name='阿坝藏族羌族自治州', province=P19)
            City.objects.create(cityid=513300, name='甘孜藏族自治州', province=P19)
            City.objects.create(cityid=513400, name='凉山彝族自治州', province=P19)

        # 贵州省
        P20 = Province.objects.get(provinceid='520000')
        if P20:
            City.objects.create(cityid=520100, name='贵阳市', province=P20)
            City.objects.create(cityid=520200, name='六盘水市', province=P20)
            City.objects.create(cityid=520300, name='遵义市', province=P20)
            City.objects.create(cityid=520400, name='安顺市', province=P20)
            City.objects.create(cityid=520500, name='毕节市', province=P20)
            City.objects.create(cityid=520600, name='铜仁市', province=P20)
            City.objects.create(cityid=522300, name='黔西南布依族苗族自治州', province=P20)
            City.objects.create(cityid=522600, name='黔东南苗族侗族自治州', province=P20)
            City.objects.create(cityid=522700, name='黔南布依族苗族自治州', province=P20)

        # 云南省
        P21 = Province.objects.get(provinceid='530000')
        if P21:
            City.objects.create(cityid=530100, name='昆明市', province=P21)
            City.objects.create(cityid=530300, name='曲靖市', province=P21)
            City.objects.create(cityid=530400, name='玉溪市', province=P21)
            City.objects.create(cityid=530500, name='保山市', province=P21)
            City.objects.create(cityid=530600, name='昭通市', province=P21)
            City.objects.create(cityid=530700, name='丽江市', province=P21)
            City.objects.create(cityid=530800, name='普洱市', province=P21)
            City.objects.create(cityid=530900, name='临沧市', province=P21)
            City.objects.create(cityid=532300, name='楚雄彝族自治州', province=P21)
            City.objects.create(cityid=532500, name='红河哈尼族彝族自治州', province=P21)
            City.objects.create(cityid=532600, name='文山壮族苗族自治州', province=P21)
            City.objects.create(cityid=532800, name='西双版纳傣族自治州', province=P21)
            City.objects.create(cityid=532900, name='大理白族自治州', province=P21)
            City.objects.create(cityid=533100, name='德宏傣族景颇族自治州', province=P21)
            City.objects.create(cityid=533300, name='怒江傈僳族自治州', province=P21)
            City.objects.create(cityid=533400, name='迪庆藏族自治州', province=P21)

        # 西藏
        P22 = Province.objects.get(provinceid='540000')
        if P22:
            City.objects.create(cityid=540100, name='拉萨市', province=P22)
            City.objects.create(cityid=540200, name='日喀则市', province=P22)
            City.objects.create(cityid=540300, name='昌都市', province=P22)
            City.objects.create(cityid=540400, name='林芝市', province=P22)
            City.objects.create(cityid=540500, name='山南市', province=P22)
            City.objects.create(cityid=542400, name='那曲地区', province=P22)
            City.objects.create(cityid=542500, name='阿里地区', province=P22)

        # 陕西省
        P23 = Province.objects.get(provinceid='610000')
        if P23:
            City.objects.create(cityid=610100, name='西安市', province=P23)
            City.objects.create(cityid=610200, name='铜川市', province=P23)
            City.objects.create(cityid=610300, name='宝鸡市', province=P23)
            City.objects.create(cityid=610400, name='咸阳市', province=P23)
            City.objects.create(cityid=610500, name='渭南市', province=P23)
            City.objects.create(cityid=610600, name='延安市', province=P23)
            City.objects.create(cityid=610700, name='汉中市', province=P23)
            City.objects.create(cityid=610800, name='榆林市', province=P23)
            City.objects.create(cityid=610900, name='安康市', province=P23)
            City.objects.create(cityid=611000, name='商洛市', province=P23)

        # 甘肃省
        P24 = Province.objects.get(provinceid='620000')
        if P24:
            City.objects.create(cityid=620100, name='兰州市', province=P24)
            City.objects.create(cityid=620200, name='嘉峪关市', province=P24)
            City.objects.create(cityid=620300, name='金昌市', province=P24)
            City.objects.create(cityid=620400, name='白银市', province=P24)
            City.objects.create(cityid=620500, name='天水市', province=P24)
            City.objects.create(cityid=620600, name='武威市', province=P24)
            City.objects.create(cityid=620700, name='张掖市', province=P24)
            City.objects.create(cityid=620800, name='平凉市', province=P24)
            City.objects.create(cityid=620900, name='酒泉市', province=P24)
            City.objects.create(cityid=621000, name='庆阳市', province=P24)
            City.objects.create(cityid=621100, name='定西市', province=P24)
            City.objects.create(cityid=621200, name='陇南市', province=P24)
            City.objects.create(cityid=622900, name='临夏回族自治州', province=P24)
            City.objects.create(cityid=623000, name='甘南藏族自治州', province=P24)

        # 青海省
        P25 = Province.objects.get(provinceid='630000')
        if P25:
            City.objects.create(cityid=630100, name='西宁市', province=P25)
            City.objects.create(cityid=630200, name='海东市', province=P25)
            City.objects.create(cityid=632200, name='海北藏族自治州', province=P25)
            City.objects.create(cityid=632300, name='黄南藏族自治州', province=P25)
            City.objects.create(cityid=632500, name='海南藏族自治州', province=P25)
            City.objects.create(cityid=632600, name='果洛藏族自治州', province=P25)
            City.objects.create(cityid=632700, name='玉树藏族自治州', province=P25)
            City.objects.create(cityid=632800, name='海西蒙古族藏族自治州', province=P25)

        # 宁夏回族自治区
        P26 = Province.objects.get(provinceid='640000')
        if P26:
            City.objects.create(cityid=640100, name='银川市', province=P26)
            City.objects.create(cityid=640200, name='石嘴山市', province=P26)
            City.objects.create(cityid=640300, name='吴忠市', province=P26)
            City.objects.create(cityid=640400, name='固原市', province=P26)
            City.objects.create(cityid=640500, name='中卫市', province=P26)

        # 新疆
        P27 = Province.objects.get(provinceid='650000')
        if P27:
            City.objects.create(cityid=650100, name='乌鲁木齐市', province=P27)
            City.objects.create(cityid=650200, name='克拉玛依市', province=P27)
            City.objects.create(cityid=650400, name='吐鲁番市', province=P27)
            City.objects.create(cityid=650500, name='哈密市', province=P27)
            City.objects.create(cityid=652300, name='昌吉回族自治州', province=P27)
            City.objects.create(cityid=652700, name='博尔塔拉蒙古自治州', province=P27)
            City.objects.create(cityid=652800, name='巴音郭楞蒙古自治州', province=P27)
            City.objects.create(cityid=652900, name='阿克苏地区', province=P27)
            City.objects.create(cityid=653000, name='克孜勒苏柯尔克孜自治州', province=P27)
            City.objects.create(cityid=653100, name='喀什地区', province=P27)
            City.objects.create(cityid=653200, name='和田地区', province=P27)
            City.objects.create(cityid=654000, name='伊犁哈萨克自治州', province=P27)
            City.objects.create(cityid=654200, name='塔城地区', province=P27)
            City.objects.create(cityid=654300, name='阿勒泰地区', province=P27)
            City.objects.create(cityid=659000, name='自治区直辖县级行政区划', province=P27)

        #北京
        s1 = Province.objects.get(provinceid=110000)
        if s1:
            City.objects.create(cityid=110101, name='东城区', province=s1)
            City.objects.create(cityid=110102, name='西城区', province=s1)
            City.objects.create(cityid=110103, name='崇文区', province=s1)
            City.objects.create(cityid=110104, name='宣武区', province=s1)
            City.objects.create(cityid=110105, name='朝阳区', province=s1)
            City.objects.create(cityid=110106, name='丰台区', province=s1)
            City.objects.create(cityid=110107, name='石景山区', province=s1)
            City.objects.create(cityid=110108, name='海淀区', province=s1)
            City.objects.create(cityid=110109, name='门头沟区', province=s1)
            City.objects.create(cityid=110111, name='房山区', province=s1)
            City.objects.create(cityid=110112, name='通州区', province=s1)
            City.objects.create(cityid=110113, name='顺义区', province=s1)
            City.objects.create(cityid=110114, name='昌平区', province=s1)
            City.objects.create(cityid=110115, name='大兴区', province=s1)
            City.objects.create(cityid=110116, name='怀柔区', province=s1)
            City.objects.create(cityid=110117, name='平谷区', province=s1)
            City.objects.create(cityid=110228, name='密云县', province=s1)
            City.objects.create(cityid=120229, name='延庆县', province=s1)

        # 天津市
        s2 = Province.objects.get(provinceid=120000)
        if s2:
            City.objects.create(cityid=120101, name='和平区', province=s2)
            City.objects.create(cityid=120102, name='河东区', province=s2)
            City.objects.create(cityid=120103, name='河西区', province=s2)
            City.objects.create(cityid=120104, name='南开区', province=s2)
            City.objects.create(cityid=120105, name='河北区', province=s2)
            City.objects.create(cityid=120106, name='红桥区', province=s2)
            City.objects.create(cityid=120107, name='塘沽区', province=s2)
            City.objects.create(cityid=120108, name='汉沽区', province=s2)
            City.objects.create(cityid=120109, name='大港区', province=s2)
            City.objects.create(cityid=120110, name='东丽区', province=s2)
            City.objects.create(cityid=120111, name='西青区', province=s2)
            City.objects.create(cityid=120112, name='津南区', province=s2)
            City.objects.create(cityid=120113, name='北辰区', province=s2)
            City.objects.create(cityid=120114, name='武清区', province=s2)
            City.objects.create(cityid=120115, name='宝坻区', province=s2)
            City.objects.create(cityid=120221, name='宁河县', province=s2)
            City.objects.create(cityid=120223, name='静海县', province=s2)
            City.objects.create(cityid=120225, name='蓟县', province=s2)

        # 上海市
        s3 = Province.objects.get(provinceid=310000)
        if s3:
            City.objects.create(cityid=120115, name='宝坻区', province=s2)
            City.objects.create(cityid=120221, name='宁河县', province=s2)
            City.objects.create(cityid=120223, name='静海县', province=s2)
            City.objects.create(cityid=120225, name='蓟县', province=s2)

        # 重庆市
        # 香港
        # 澳门
        # 台湾











