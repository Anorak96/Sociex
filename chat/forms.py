from django import forms
from .models import Chat, Image
    
class ChatForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'style': 'padding: 10px; resize: none; margin-right:9px;'}), required=False)
        
    class Meta:
        model = Chat
        fields = [
            'body',
        ]

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class ImageForm(forms.ModelForm):
    image = MultipleFileField(widget=MultipleFileInput())

    class Meta:
        model = Image
        fields = ('image',)