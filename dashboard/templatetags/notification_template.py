from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from customer.models import Notification, NotificationRead

register = template.Library()

@register.filter(is_safe=True)
def get_notification_state(id,user):
    try:
        notificationread = NotificationRead.objects.filter(notification_id=id,user=user).first()
        return notificationread.read
    except:
        return False

@register.filter(is_safe=True)
def get_unread_notification(user):
    read_notifications = NotificationRead.objects.filter(user=user)
    queryset = Notification.objects.all().exclude(id__in=read_notifications.values_list('notification_id',flat=True))
    return queryset
