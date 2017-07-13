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
        fields = ['building', 'unit', 'floor', 'room_num', 'price', 'total']

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
                user = User.objects.create_user(username=instance.mobile,
                                                password=instance.identication)
                user.custom = instance
                user.is_admin = False
                user.save()
                return instance


class HouseTypeForm(forms.ModelForm):

    class Meta:
        model = HouseType
        fields = ['name', 'pic', 'num']

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.event = self.initial['event']
            instance = super(HouseTypeForm, self).save(commit)
            return instance
