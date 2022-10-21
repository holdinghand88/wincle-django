from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, reverse, redirect
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db import models, transaction
from core.customfields import ULIDField, TranslatedField
from simple_history.models import HistoricalRecords
from django.utils import timezone
from datetime import datetime
import pytz
import pyotp
import ulid
import unicodedata
from django.conf import settings
from dashboard.models import User,Account
from customer.models import Customer

class BroadcastHistory(models.Model):    
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    target = models.CharField(verbose_name=_('配信先'),max_length=50,default="すべての友だち")
    customer = models.ManyToManyField(Customer,blank=True, null=True)
    amount = models.IntegerField(default=1)
    is_push = models.BooleanField(default=True)
    file_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    # CUD履歴管理
    history = HistoricalRecords(cascade_delete_history=True)
    
    def __repr__(self):
        return str(self.customer.name)