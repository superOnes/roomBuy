from django.db import models


class Event(models.Model):
    APT = 1
    PARKING = 2
    TYPES = (
        (APT, '房间开盘'),
        (PARKING, '车位开盘'),
    )
    type = models.PositiveSmallIntegerField('活动类型', choices=TYPES, default=APT)
    name = models.CharField('活动名称', max_length=100)
    phone_num = models.CharField('咨询电话', max_length=50, null=True, blank=True)
    test_start = models.DateTimeField('公测开始时间')
    test_end = models.DateTimeField('公测结束时间')
    test_price = models.BooleanField('是否显示公测放假', default=False)
    event_start = models.DateTimeField('活动开始时间')
    event_end = models.DateTimeField('活动结束时间')
    limit = models.IntegerField('选房完成期限')
    equ_login_num = models.IntegerField('支持设备登录数')
    follow_num = models.IntegerField('同一账号允许收藏数')
    login_msg = models.BooleanField('登录短信提醒', default=False)
    price = models.BooleanField('是否显示原价', default=False)
    covered_space = models.BooleanField('是否显示建筑面积', default=False)
    covered_space_price = models.BooleanField('是否显示建筑面积单价', default=False)
    inside_space = models.BooleanField('是否显示套内面积', default=False)
    inside_space_price = models.BooleanField('是否显示套内面积单价', default=False)
    description = models.TextField('活动细则')
    notice = models.TextField('认购须知')
    tip = models.TextField('温馨提示')
    cover = models.ImageField('活动封面', upload_to='cover/%Y/%m/%d/',
                              null=True, blank=True)
    plane_graph = models.ImageField('平面图', upload_to='planeGraph/%Y/%m/%d/',
                                    null=True, blank=True)
    term = models.TextField('协议')
