from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
   # path("<str:room_name>/", views.room, name="room"),
    path('chatroom/', views.rooms_view, name='rooms'),
    path('create_chatroom/', views.ChatroomCreateView.as_view(), name='create_chatroom'),
    path('chatroom/<str:chatroom_name>/', views.chatroom_view, name='chatroom'),
    path('private/<int:recipient_id>/', views.private_message_view, name='private_message'),
]
