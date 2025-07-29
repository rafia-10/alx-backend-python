from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Message, Conversation
from .serializers import MessageSerializer
from rest_framework.decorators import action
from rest_framework.status import HTTP_403_FORBIDDEN

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        user = self.request.user

        # Check if user is part of the conversation
        if not Conversation.objects.filter(id=conversation_id, participants=user).exists():
            raise PermissionDenied(detail="You're not part of this conversation", code=HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You're not part of this conversation", code=HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)
