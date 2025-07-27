from rest_framework import serializers
from .models import user, message, conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields = ['user_id', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    class Meta:
        model = conversation
        fields = ['participants', 'created_at', 'message','conversation_id' ]

    def get_messages(self, obj):
        msgs = message.objects.filter(sender__in=obj.participants.all()).order_by('-sent_at')
        return MessageSerializer(msgs, many=True).data



