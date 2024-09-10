from django import forms
from .models import Message, Chatroom


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class ChatroomForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        fields = ['name']

