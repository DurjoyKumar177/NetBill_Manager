from django import forms
from .models import Complain, Reply

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['title', 'categories', 'body', 'attachment']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message', 'attachment']
