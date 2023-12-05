from django import forms
from .models import Group, Message

class GroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'style': 'padding: 10px; resize: none;'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'style': 'padding: 10px; resize: none;'}), required=False)

    class Meta:
        model = Group
        fields = [
            'name',
            'description',
        ]

class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'style': 'padding: 10px; resize: none;'}), required=False)

    class Meta:
        model = Message
        fields = [
            'body',
        ]

class GroupUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'style': 'padding: 10px; resize: none;'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'style': 'padding: 10px; resize: none;'}), required=False)

    class Meta:
        model = Group
        fields = [
            'name',
            'description',
            'created_by',
            'mods',
            'members'
        ]