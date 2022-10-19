from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from item.models import ItemCategory,Item

register = template.Library()

@register.filter(is_safe=True)
def get_item_category(account):
    return ItemCategory.objects.filter(account=account)

@register.filter(is_safe=True)
def get_item_list(account):
    return Item.objects.filter(account=account)
