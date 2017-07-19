import uuid
from django import forms
from django.db import transaction
from .models import Event, EventDetail, HouseType
from accounts.models import Customer, User


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [f.name for f in model._meta.fields]


class EventDetailForm(forms.ModelForm):

    class Meta:
        model = EventDetail
        fields = ['building', 'unit', 'floor', 'room_num', 'price', 'area']

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.event = self.initial['event']
            instance = super(EventDetailForm, self).save(commit)
            return instance


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['realname', 'mobile', 'identication', 'count', 'remark']

    def save(self, commit=True):
        if not self.instance.id:
            with transaction.atomic():
                self.instance.event = self.initial['event']
                instance = super(CustomerForm, self).save(commit)
                User.objects.create_user(username=instance.mobile,
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
        num_list = HouseType.objects.filter(event=self.cleaned_data['event']) \
                                    .values_list('num', flat=True)
        if self.cleaned_data['num'] in num_list:
            raise forms.ValidationError('户型编码不能重复')
        return self.cleaned_data['num']
