from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'message', MessageViewSet)
router.register(r'conversation', ConversationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    ]