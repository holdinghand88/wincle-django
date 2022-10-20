from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from customer.models import Customer
from dashboard.models import User, Account

register = template.Library()

@register.filter(is_safe=True)
def get_customer(id):
    try:
        customer = Customer.objects.get(id=id)
        return customer
    except:
        return []

@register.filter(is_safe=True)
def get_user(id):
    try:
        user = User.objects.get(id=id)
        return user
    except:
        return []
    
@register.filter(is_safe=True)
def get_account(id):
    try:
        account = Account.objects.get(user_id=id)
        return account
    except:
        return []