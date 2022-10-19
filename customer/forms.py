from django import forms
from customer.models import Customer
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from django.core.exceptions import ValidationError
import pytz

class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'
    
class CustomerForm(forms.ModelForm):    
    name = forms.CharField(label='名字', required=True)
    account_id = forms.IntegerField(required=True)
    line_name = forms.CharField(label='ライン名', required=True)
    birthday = forms.DateField(label='Birthday', required=False)
    address = forms.CharField(label='住所', required=True)
    gender = forms.IntegerField(label='性別', required=True)
    point = forms.IntegerField(label='ポイント', required=False)
    memo = forms.Textarea()   
    
    class Meta:
        model = Customer
        fields = ("name","account_id", "line_name","gender","birthday","address", "point", "memo")
        
    def __init__(self, pk, *args, **kwargs):
        self.pk = pk
        super(CustomerForm, self).__init__(*args, **kwargs)
        
    def clean(self):        
        customer = get_object_or_404(Customer, id=self.pk)
        if customer.name == self.cleaned_data['name']:
            pass
        else:
            try:
                customer = Customer.objects.filter(name=self.cleaned_data['name'],account_id=self.cleaned_data["account_id"])
                if len(customer) > 0:
                    print("同じメールを持つユーザーが既に存在します。")
                    raise forms.ValidationError("同じメールを持つユーザーが既に存在します。")
            except Customer.DoesNotExist:
                pass  
    
    def update(self, pk):
        customer = get_object_or_404(Customer, id=pk)
        try:            
            customer.name = self.cleaned_data["name"]
            customer.gender = self.cleaned_data["gender"]
            customer.line_name = self.cleaned_data["line_name"]
            customer.birthday = self.cleaned_data["birthday"]            
            customer.point = self.cleaned_data["point"]
            customer.memo = self.cleaned_data["memo"]            
            customer.updated_at = datetime.today().astimezone(pytz.timezone('Asia/Tokyo'))
            customer.save()
            return customer
        except:
            return customer
    
class AddCustomerCreateForm(forms.ModelForm):    
    name = forms.CharField(label='名字', required=True)
    account_id = forms.IntegerField(required=True)
    line_name = forms.CharField(label='ライン名', required=True)
    birthday = forms.DateField(label='Birthday', required=False)
    address = forms.CharField(label='住所', required=True)
    gender = forms.IntegerField(label='性別', required=True)
    point = forms.IntegerField(label='ポイント', required=False)
    memo = forms.Textarea()    
    
    class Meta:
        model = Customer
        fields = ("name", "account_id", "line_name","gender","birthday","address", "point", "memo")
        
    def clean(self):        
        try:
            customer = Customer.objects.filter(name=self.cleaned_data['name'],account_id=self.cleaned_data["account_id"])
            if len(customer) > 0:
                print("同じ名前を持つユーザーが既に存在します。")
                raise forms.ValidationError("同じ名前を持つユーザーが既に存在します。")
        except Customer.DoesNotExist:
            pass
        
    def save(self, commit=True):
        customer = Customer()
        customer.name = self.cleaned_data["name"]
        customer.account_id = self.cleaned_data["account_id"]
        customer.line_name = self.cleaned_data["line_name"]
        customer.birthday = self.cleaned_data["birthday"]
        customer.address = self.cleaned_data["address"]
        customer.gender = self.cleaned_data["gender"]
        customer.point = self.cleaned_data["point"]        
        customer.memo = self.cleaned_data["memo"]        
        customer.save()
        
        return customer

