from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models, transaction
from core.customfields import ULIDField, TranslatedField
from django.utils import timezone
from datetime import datetime
import pytz
import pyotp
import ulid
import unicodedata
from django.conf import settings

# 支払い方法
HowtoPayChoices = (1, "LINEPay"), (2, "銀行振込"), (3, "クレジットカード"), (4, "代引き"), (5, "店舗で決済"), (6, "着払い")
