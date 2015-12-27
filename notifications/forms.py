from django import forms

from models import NotificationRegistry


class NotificationRegistryForm(forms.ModelForm):



    class Meta:
        model = NotificationRegistry
        fields = (
            'threads',
            'categories'
        )
