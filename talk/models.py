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

class Talk(models.Model):    
    content = models.TextField()
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    is_push = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __repr__(self):
        return str(self.customer.name)