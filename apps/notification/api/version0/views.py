from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.notification.api.version0.serializers import NotificationSerializer
from apps.notification.models import Notification


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(NotificationListAPIView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    @swagger_auto_schema(
        operation_id='Notifications list',
        operation_description='Retrieve a list of notifications for the authenticated user.',
        tags=['Notifications'],
        responses={200: NotificationSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class NotificationRetrieveAPIView(RetrieveAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = super(NotificationRetrieveAPIView, self).get_object()
        if not obj.read:
            obj.read = True
            obj.save()
        return obj

    @swagger_auto_schema(
        operation_id='Retrieve list',
        tags=['Notifications'],
        operation_description="Retrieve a specific notification by its ID. The notification is marked as read upon retrieval.",
        responses={200: NotificationSerializer()}
    )
    def get(self, request, *args, **kwargs):
        """
        Get a specific notification.
        """
        return super().get(request, *args, **kwargs)


notification_list = NotificationListAPIView.as_view()
notification_retrieve = NotificationRetrieveAPIView.as_view()
