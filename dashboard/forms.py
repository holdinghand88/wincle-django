from django import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress
from .models import User,Account
from datetime import datetime
from django.contrib.auth.forms import (
    AuthenticationForm,PasswordResetForm,UsernameField
)

class AddUserCreateForm(UserCreationForm):
    email = forms.EmailField(label="メールアドレス", required=True)
    name = forms.CharField(label='店舗名',required=False)
    referral_code = forms.CharField(label='ブランドコード',required=False)
    password1 = forms.CharField(label='パスワード', required=True, strip=False, widget=forms.PasswordInput())
    password2 = forms.CharField(label='パスワード確認', required=True, strip=False, widget=forms.PasswordInput())
    is_multiple = forms.BooleanField(required=False)
    channel_id = forms.CharField(label='channel_id', required=False)
    channel_secret = forms.CharField(label='channel_secret', required=False) 
    access_token = forms.CharField(label='access_token', required=False) 
    
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "is_multiple")
        
    def clean(self):        
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            print("同じメールを持つユーザーが既に存在します。")
            raise forms.ValidationError("同じメールを持つユーザーが既に存在します。")
        except User.DoesNotExist:
            pass
        
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2 
        
    def save(self, commit=True):
        user = User()
        user.email = self.cleaned_data["email"]        
        user.password = make_password(self.cleaned_data["password1"])
        is_multiple = self.cleaned_data["is_multiple"]
        if is_multiple:
            user.referral_code = self.cleaned_data["referral_code"]
            user.is_staff = True
            user.is_multiple = True
        user.is_active = True
        user.save()
        allauth_emailconfirmation = EmailAddress(user=user, email=self.cleaned_data["email"], verified=True, primary=True)
        allauth_emailconfirmation.save()
        
        
        return user

class AddChildUserCreateForm(UserCreationForm):
    email = forms.EmailField(label="メールアドレス", required=True)
    name = forms.CharField(label='店舗名', required=True) 
    referral_code = forms.CharField(label='ブランドコード', required=True)       
    password1 = forms.CharField(label='パスワード', required=True, strip=False, widget=forms.PasswordInput())
    password2 = forms.CharField(label='パスワード確認', required=True, strip=False, widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "referral_code")
        
    def clean(self):        
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            print("同じメールを持つユーザーが既に存在します。")
            raise forms.ValidationError("同じメールを持つユーザーが既に存在します。")
        except User.DoesNotExist:
            pass        
        
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2 
        
    def save(self, commit=True):
        user = User()
        user.email = self.cleaned_data["email"]        
        user.password = make_password(self.cleaned_data["password1"])
        user.referral_code = self.cleaned_data["referral_code"]
        user.is_active = True
        user.save()
        allauth_emailconfirmation = EmailAddress(user=user, email=self.cleaned_data["email"], verified=True, primary=True)
        allauth_emailconfirmation.save()
        
        return user
