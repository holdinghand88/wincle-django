import ulid
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import translation
from django.utils.translation import gettext_lazy as _


class ULIDField(models.CharField):
    """ULIDフィールドの定義"""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 26
        super(ULIDField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'char(26)'


class TranslatedField(object):
    """多言語切り替え用フィールドの定義"""

    def __init__(self, ja_field, en_field, zh_hant_field, zh_hans_field):
        self.ja_field = ja_field
        self.en_field = en_field
        self.zh_hant_field = zh_hant_field
        self.zh_hans_field = zh_hans_field

    def __get__(self, instance, owner):

        # 現在有効な言語（i18n）を取得
        active_language = translation.get_language()

        # 英語の場合は英語フィールドを利用し、それ以外は日本語のフィールドを使用
        if active_language == 'en':
            return getattr(instance, self.en_field)
        elif active_language == 'zh-hant':
            return getattr(instance, self.zh_hant_field)
        elif active_language == 'zh-hans':
            return getattr(instance, self.zh_hans_field)

        return getattr(instance, self.ja_field)
