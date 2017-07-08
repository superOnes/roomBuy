from django import forms
from .models import EventDetail


class EventDetailForm(forms.ModelForm):

    class Meta:
        model = EventDetail
        fields = ['building', 'unit', 'floor', 'room_num', 'price', 'total']

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.event = self.initial['event']
            instance = super(EventDetailForm, self).save(commit)
            return instance
