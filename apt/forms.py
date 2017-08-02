import uuid
import time
from datetime import datetime

from django import forms
from django.db import transaction
from .models import Event, EventDetail, HouseType
from accounts.models import Customer, User, Order


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['equ_login_num']

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if not self.instance.id:
            if cleaned_data['test_start'] < datetime.now():
                raise forms.ValidationError('公测开始时间不得早于当前时间！')
        if cleaned_data['test_start'] >= cleaned_data['test_end']:
            raise forms.ValidationError('公测结束时间不能提前于公测开始时间！')
        if cleaned_data['event_start'] < cleaned_data['test_end']:
            raise forms.ValidationError('活动开始时间不得早于公测结束时间！')
        if cleaned_data['event_start'] >= cleaned_data['event_end']:
            raise forms.ValidationError('活动结束时间不能提前于活动开始时间！')
        return cleaned_data


class EventDetailForm(forms.ModelForm):
    class Meta:
        model = EventDetail
        fields = ['building', 'unit', 'floor', 'room_num', 'looking',
                  'unit_price', 'term', 'area']

    def clean(self):
        cleaned_data = super(EventDetailForm, self).clean()
        event = self.initial['event']
        current_user = self.initial['current_user']
        eventdetail = EventDetail.objects.all()
        print(eventdetail)
        for ed in eventdetail:
            if cleaned_data['building'] == ed.building \
                    and cleaned_data['unit'] == ed.unit \
                    and cleaned_data['floor'] == ed.floor \
                    and cleaned_data['room_num'] == ed.room_num:
                raise forms.ValidationError('该车位/房源已存在！')
        if event.eventdetail_set.count() >= int(current_user.house_limit):
            raise forms.ValidationError('车位/房源数量超出上限，不可添加')
        return cleaned_data

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.event = self.initial['event']
            instance = super(EventDetailForm, self).save(commit)
            return instance


class EventDetailSignForm(forms.ModelForm):
    class Meta:
        model = EventDetail
        fields = ['sign']

    def clean_sign(self):
        if self.instance.event.is_pub:
            raise forms.ValidationError('该活动已经发布，不能备注')
        customer = self.cleaned_data['sign']
        if customer:
            if Order.objects.filter(eventdetail=self.instance,
                                    is_test=False).exists():
                raise forms.ValidationError('该房源或车位已被选购')
            elif customer.user.order_set.count() >= customer.count:
                raise forms.ValidationError('该用户已购房')
        return customer

    def save(self):
        with transaction.atomic():
            instance = super(EventDetailSignForm, self).save()
            if instance.sign is None:
                if self.initial['object'].sign:
                    Order.objects.filter(user=self.initial['object'].sign.user,
                                         eventdetail=instance,
                                         is_test=False).delete()
                    if instance.is_sold is True:
                        instance.is_sold = False
                        instance.save()
            else:
                Order.objects.create(user=instance.sign.user,
                                     eventdetail=instance,
                                     order_num=time.strftime('%Y%m%d%H%M%S'),
                                     is_test=False)
            return instance


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['realname', 'mobile', 'identication', 'remark']

    def save(self, commit=True):
        if not self.instance.id:
            with transaction.atomic():
                self.instance.event = self.initial['event']
                instance = super(CustomerForm, self).save(commit)
                User.objects.create_user(username=uuid.uuid1(),
                                         password=instance.identication,
                                         customer=instance,
                                         is_admin=False)
                return instance


class HouseTypeForm(forms.ModelForm):
    class Meta:
        model = HouseType
        fields = ['event', 'name', 'pic', 'num']

    def clean_event(self):
        if not self.instance.id:
            return self.initial['event']
        return self.cleaned_data['event']

    def clean_num(self):
        if not self.instance.id:
            ht = HouseType.objects.filter(event=self.cleaned_data['event'])
        else:
            ht = HouseType.objects.filter(event=self.cleaned_data['event']) \
                .exclude(id=self.instance.id)
        if ht and self.cleaned_data['num'] in ht.values_list('num', flat=True):
            raise forms.ValidationError('户型编码不能重复')
        return self.cleaned_data['num']
