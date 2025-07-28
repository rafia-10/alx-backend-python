from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(permissions.BasePermission):
    """
    Custom permission: only allow users to access their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.sender == request.user or obj.receiver == request.user


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify messages.
    """

    def has_permission(self, request, view):
        
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        This is where we check if the user is part of the conversation.
        Assumes `obj` is a Message instance and has a `conversation` field
        which itself has a `participants` ManyToMany field.
        """
        return request.user in obj.conversation.participants.all()
