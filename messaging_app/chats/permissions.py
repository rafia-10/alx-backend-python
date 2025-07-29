from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(permissions.BasePermission):
    """
    Custom permission: only allow users to access their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.sender == request.user or obj.receiver == request.user


    def has_permission(self, request, view):
        # Allow safe methods for all users
        if request.method in SAFE_METHODS:
            return True
        
        # For unsafe methods, check if the user is authenticated
        return request.user and request.user.is_authenticated

class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        return request.user in obj.conversation.participants.all()

    def has_permission(self, request, view):
        # For write methods, allow only participants
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            conversation_id = request.data.get("conversation")
            if conversation_id:
                from chats.models import Conversation  # local import to avoid circular issues
                try:
                    convo = Conversation.objects.get(id=conversation_id)
                    return request.user in convo.participants.all()
                except Conversation.DoesNotExist:
                    return False
        return True
