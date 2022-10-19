from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db import models, transaction
from core.customfields import ULIDField, TranslatedField
from django.utils import timezone
from datetime import datetime
import pytz
import pyotp
import ulid
import unicodedata
from django.conf import settings
from dashboard.models import User,Account

# Genderのラジオボタン用
GenderChoices = (1, "男性"), (2, "女性")

class Customer(models.Model):
    """Customer"""
    id = ULIDField(
        default=ulid.new,
        primary_key=True,
        editable=False
    )
    account = models.ForeignKey(Account,on_delete=models.CASCADE)   
    name = models.CharField(_('名前'), max_length=50, blank=True, null=True)
    line_name = models.CharField(verbose_name=_('ライン名'),max_length=50,blank=True, null=True)
    line_id = models.CharField(verbose_name=_('ラインID'),max_length=50,blank=True, null=True)   
    avatar = models.ImageField(upload_to="user_avatars",blank=True, null=True)
    gender = models.IntegerField(_(u'性別'), choices=GenderChoices,default=1)
    birthday = models.DateField(_(u'生年月日'),blank=True, null=True)
    address = models.CharField(_('住所'), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_('郵便番号'), max_length=50, blank=True, null=True)
    tel = models.CharField(_('電話番号'), max_length=50, blank=True, null=True)
    point = models.IntegerField(_(u'保有ポイント数'), default=0)
    memo = models.TextField(_('メモ'),blank=True, null=True)
    isTalking = models.BooleanField(default=True)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    tags = models.JSONField(verbose_name=_(u'タグ'),blank=True, null=True)   
    is_leave = models.BooleanField(default=False) 
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    created_at = models.DateTimeField(_(u'Created Date At'), editable=False, auto_now_add=True)
    created_by = models.CharField(_(u'Created Person By'), max_length=26, blank=True, null=True)
    updated_at = models.DateTimeField(_(u'Updated Date At'), blank=True, null=True)
    updated_by = models.CharField(_(u'Updated Person By'), max_length=26, blank=True, null=True)
    deleted_at = models.DateTimeField(_(u'Deleted Date At'), blank=True, null=True)
    deleted_by = models.CharField(_(u'Deleted Person By'), max_length=26, blank=True, null=True)
    
    def __str__(self):
        return self.name

class NotificationAction(models.Model):
    '''
    ユーザーのアクション
    1. 商品購入
    2. トーク
    3. 
    
    '''
    name = models.CharField(max_length=50)
    effect = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Notification(models.Model):
    
    class Meta:
        ordering = ['-created_at']
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    action = models.ForeignKey(NotificationAction,on_delete=models.CASCADE)    
    created_at = models.DateTimeField(_(u'Created Date At'), editable=False, auto_now_add=True)
    
    def __str__(self):
        return self.action.name+'by'+self.user.last_name_jp
    
    @property
    def notification_text(self):
        return self.customer.name() + '様の【' + self.action.name + '】アクションがありました。'
    
    
class NotificationRead(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification,on_delete=models.CASCADE)
    read = models.BooleanField(default=True)
    created_at = models.DateTimeField(_(u'Created Date At'), editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.notification.action.name+'by'+self.notification.customer.name
