from django.shortcuts import render, redirect
from .models import Chatroom, Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatroomForm


def test(request):
    return render(request, 'test.html')



def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})

@login_required
def chatroom_view(request, chatroom_name):
    chatroom = Chatroom.objects.get(name=chatroom_name)
    messages = Message.objects.filter(chatroom=chatroom).order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.chatroom = chatroom
            msg.save()
            return redirect('chatroom', chatroom_name=chatroom_name)
    else:
        form = MessageForm()
    return render(request, 'chat_room.html', {'chatroom': chatroom, 'messages': messages, 'form': form})


@login_required
def private_message_view(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(sender=request.user, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=request.user)
    messages = messages.order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            return redirect('private_message', recipient_id=recipient_id)
    else:
        form = MessageForm()
    return render(request, 'private_message.html', {'recipient': recipient, 'messages': messages, 'form': form})


@login_required
def rooms_view(request):
    chatrooms = Chatroom.objects.all()
    users = User.objects.filter(is_active=True)
    return render(request, 'rooms.html', {'chatrooms': chatrooms, 'users': users})


class ChatroomCreateView(LoginRequiredMixin, CreateView):
    model = Chatroom
    form_class = ChatroomForm
    template_name = 'create_chatroom.html'
    success_url = reverse_lazy('rooms')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response


