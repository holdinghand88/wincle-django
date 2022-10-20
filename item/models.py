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

class ItemCategory(models.Model):
    """商品カテゴリー"""    
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    

class Item(models.Model):
    id = ULIDField(
        default=ulid.new,
        primary_key=True,
        editable=False
    )
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    # --------------------------------------------------------------------------------------------------------------
    # 内部用の管理情報
    # --------------------------------------------------------------------------------------------------------------
    # 資材管理番号
    material_control_id = models.CharField(max_length=26, blank=True, null=True)
    # 商品区分
    item_classification = models.CharField(max_length=26, blank=True, null=True)
    # 送料無料フラグ
    free_shippingflg = models.BooleanField(default=False, )
    # 商品の出荷対象フラグ
    shipment_targetflg = models.BooleanField(default=True, )
    is_discount = models.BooleanField(_(u'セール'), default=False, )
    sale_sdate = models.DateField(_(u'セール期間'), blank=True, null=True)
    sale_edate = models.DateField(_(u'セール期間'), blank=True, null=True)
    publish = models.BooleanField(default=True)   
    max_point= models.IntegerField(_(u'利用ポイント上限数'),default=100)
    order_max_quantity= models.IntegerField(_(u'最大注文可能個数'),default=3)
    # ==============================================================================================================
    # 1. 商品基本情報（商品写真・商品名・商品紹介情報・カテゴリー・JANコード等など）
    # ==============================================================================================================
    # --------------------------------------------------------------------------------------------------------------
    # (1)商品基本情報
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ItemCategory,on_delete=models.CASCADE)
    # 商品内容・内容量・サイズ表記    
    description = models.TextField(blank=True, null=True)
    itemcontents_displayflg = models.BooleanField(default=True)
    # --------------------------------------------------------------------------------------------------------------
    # 商品画像_簡易
    image1 = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)
    image6 = models.ImageField(blank=True, null=True)
    image7 = models.ImageField(blank=True, null=True)
    image8 = models.ImageField(blank=True, null=True)
    image9 = models.ImageField(blank=True, null=True)
    image10 = models.ImageField(blank=True, null=True)
    # 商品数量単位
    item_quantity_unit_name = models.CharField(max_length=26, blank=True, default="個")
    # 商品数量
    quantity = models.IntegerField(_(u'在庫数'),default=0)
    #価格
    dec_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dec_origin_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dec_sale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    origin_price = models.IntegerField(blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    discount_price = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)    
    
    # CUD履歴管理
    history = HistoricalRecords(cascade_delete_history=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("item:item-detail", kwargs={
            'pk': self.id
        })
        
class Item_types(models.Model):
    name = models.CharField(_(u'種類'),max_length=100)
    stock = models.IntegerField(_(u'在庫数'),default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    

class OrderItem(models.Model):
    id = ULIDField(
        default=ulid.new,
        primary_key=True,
        editable=False
    )
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    
    # CUD履歴管理
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.item.title}の{self.quantity}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    

class Order(models.Model):
    id = ULIDField(
        default=ulid.new,
        primary_key=True,
        editable=False
    )
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    receive_date = models.DateTimeField(blank=True, null=True)
    pay_status = models.BooleanField(default=False)
    how_to_pay = models.JSONField(_(u'支払い方法'), blank=True, null=True)
    how_to_receive = models.CharField(_(u'受取方法'), blank=True, null=True,max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    # CUD履歴管理
    history = HistoricalRecords()
    
    def __str__(self):
        return self.account.name
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
