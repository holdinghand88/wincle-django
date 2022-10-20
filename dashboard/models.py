from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models, transaction
from core.customfields import ULIDField, TranslatedField
from core.models import HowtoPayChoices
from django.utils import timezone
from datetime import datetime
import pytz
import pyotp
import ulid
import unicodedata
from allauth.account.models import EmailAddress
from simple_history.models import HistoricalRecords
from django.conf import settings

class UserManager(BaseUserManager):    
    
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves User with the given email and password. """
        now = datetime.today().astimezone(pytz.timezone('Asia/Tokyo'))
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(
            #username=email,
            email=email,
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields
        )        
        user.account_type = 2
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    # def create_superuser(self, username, email, password, **extra_fields):
    def create_superuser(self, email, password, **extra_fields):
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.account_type = 1        
        user.created_by = 0        
        user.is_superuser = True

        # ========================================================================================
        # User、django-allauthのEmailAddressテーブル保存処理のトランザクション開始--->>>
        # ========================================================================================
        with transaction.atomic():

            user.save(using=self._db)

            # --------------------------------------------------------------------------------------------
            #  django-allauthのEmailAddressテーブルの新規登録情報を設定して保存
            # --------------------------------------------------------------------------------------------
            allauth_emailconfirmation = EmailAddress(user=user, email=email, verified=True, primary=True)

            # django-allauthのEmailAddressへの保存処理
            allauth_emailconfirmation.save()

        # ========================================================================================
        # <<<--- User、django-allauthのEmailAddressテーブル保存処理のトランザクション終了
        # ========================================================================================

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User"""
    id = ULIDField(
        default=ulid.new,
        primary_key=True,
        editable=False
    )
    account_type = models.CharField(max_length=26, blank=True, null=True)
    email = models.EmailField(verbose_name=_(u'email address'), max_length=50, unique=True)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    customer_columns = models.JSONField(blank=True, null=True)
    is_multiple = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    created_at = models.DateTimeField(_(u'Created Date At'), editable=False, auto_now_add=True)
    created_by = models.CharField(_(u'Created Person By'), max_length=26, blank=True, null=True)
    updated_at = models.DateTimeField(_(u'Updated Date At'), blank=True, null=True)
    updated_by = models.CharField(_(u'Updated Person By'), max_length=26, blank=True, null=True)
    deleted_at = models.DateTimeField(_(u'Deleted Date At'), blank=True, null=True)
    deleted_by = models.CharField(_(u'Deleted Person By'), max_length=26, blank=True, null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email
    
    @property
    def username(self):
        return self.email
    
 
class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(_('店舗名'), max_length=50,blank=True,null=True)
    channel_id = models.CharField(verbose_name=_('channel_id'),max_length=255,blank=True,null=True)   
    channel_secret = models.CharField(verbose_name=_('channel_secret'),max_length=255,blank=True,null=True)  
    access_token = models.CharField(verbose_name=_('access_token'),max_length=255,blank=True,null=True)  
    address = models.CharField(_('住所'), max_length=255, blank=True, null=True)
    sdates = models.DateField(blank=True, null=True)
    edates = models.DateField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    instagram_id = models.CharField(verbose_name=_('instagram_id'),max_length=255,blank=True,null=True)
    line_url = models.URLField(verbose_name=_('line_url'),max_length=255,blank=True, null=True)
    avatar = models.ImageField(upload_to="account_avatars",blank=True, null=True)
    description = models.TextField(_('アカウント紹介文'),blank=True, null=True)    
    notify_token = models.CharField(verbose_name=_('notify_token'),max_length=255,blank=True, null=True)
    referral_point = models.IntegerField(_(u'referral_point'), default=0)
    is_duplicate = models.BooleanField(default=False)
    deadline_day = models.IntegerField(default=20)    
    is_richmenu = models.BooleanField(default=True)
    email_notification = models.BooleanField(verbose_name=_(u'メール設定'),default=True)
    
    #物販設定
    item_categories = models.JSONField(_(u'商品カテゴリー'),blank=True, null=True)
    reduction_rate = models.DecimalField(_(u'ポイント還元率'), max_digits=8, decimal_places=2, default=0)
    how_to_pay = models.JSONField(_(u'支払い方法'), blank=True, null=True)
    pay_channel_id = models.CharField(verbose_name=_('pay_channel_id'),max_length=255,blank=True, null=True)
    pay_channel_secret = models.CharField(verbose_name=_('pay_channel_secret'),max_length=255,blank=True, null=True)    
    bank_info = models.CharField(_('銀行振込先'), max_length=255, blank=True, null=True)    
    max_ec_point = models.IntegerField(_(u'使用上限ポイント'), default=30000)
    is_ec_point = models.BooleanField(default=True)
    postage = models.IntegerField(default=0)
    postage_free_border = models.IntegerField(default=0)
    is_inventory_view = models.BooleanField(verbose_name=_('在庫数表示'),default=True)
    is_soldout_notice = models.BooleanField(verbose_name=_('売り切れalarm'),default=True)
    is_soldout_view = models.BooleanField(verbose_name=_('売り切れ表示'),default=True)
    
    # CUD履歴管理
    history = HistoricalRecords(cascade_delete_history=True)
    
    def __str__(self):
        return self.user.email
    
    
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()
