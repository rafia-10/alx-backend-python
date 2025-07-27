from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission

class user(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, 
                            choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
                             null=False )
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # <- give it a unique name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # <- another unique name
        blank=True
    )

class message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(user, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
