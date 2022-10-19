from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from customer.models import Customer

register = template.Library()

@register.filter(is_safe=True)
def get_customer(id):
    try:
        customer = Customer.objects.get(id=id)
        return customer
    except:
        return False
