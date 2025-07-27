from django.shortcuts import render
from rest_framework import viewsets
from .models import message, conversation
from .serializers import ConversationSerializer,MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = conversation.objects.all()
    serializer_class = ConversationSerializer

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)