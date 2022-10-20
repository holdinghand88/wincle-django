from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from ..models import User,Account
from ..forms import AddUserCreateForm,AddChildUserCreateForm
from ..permissions import SuperUserCheck,StaffUserCheck
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from item.models import Item

class UserManageView(SuperUserCheck,ListView):
    model = User
    paginate_by = 10
    template_name = 'user/userlist.html'
    
    def get_queryset(self, **kwargs):
        return User.objects.all().order_by('-id')
    
@user_passes_test(lambda u: u.is_superuser)  
def inactive(request):
    pk = request.POST.get('user_id')
    user = get_object_or_404(User, id=pk)
    active_status = user.is_active
    if active_status:
        active_status = 0
    else:
        active_status = 1
    user.is_active = active_status
    user.save()
    resp = HttpResponse(f'{{"active_status": "{user.is_active}"}}')
    resp.content_type = "application/json"
    resp.status_code = 200
    return resp

@login_required  
def deletuser(request, pk):
    user = get_object_or_404(User, id=pk)
    
    user.delete()
    if request.user.is_superuser:
        return redirect(reverse("dashboard:usermanage"))
    else:
        return redirect(reverse("dashboard:childusermanage"))

@user_passes_test(lambda u: u.is_superuser)  
def addnewuser(request):
    form = AddUserCreateForm(request.POST)    
    if form.is_valid():
        user = form.save()
        account = get_object_or_404(Account, user_id=user.id)
        account.user = user
        account.name = form.cleaned_data["name"]
        account.channel_id = form.cleaned_data["channel_id"]
        account.channel_secret = form.cleaned_data["channel_secret"]
        account.access_token = form.cleaned_data["access_token"]
        account.save()
        return redirect(reverse("dashboard:usermanage"))
    else:
        print("failed")
        return redirect(reverse("dashboard:usermanage"))
    
@user_passes_test(lambda u: u.is_superuser)  
def childaddnewuser(request):
    form = AddChildUserCreateForm(request.POST)     
    if form.is_valid():
        user = form.save()
        account = get_object_or_404(Account, user_id=user.id)
        account.user = user
        account.name = form.cleaned_data["name"]        
        account.save()
        return redirect(reverse("dashboard:usermanage"))
    else:
        print("failed")
        return redirect(reverse("dashboard:usermanage"))

@user_passes_test(lambda u: u.is_superuser) 
def userinfoupdate(request,pk):
    try:        
        name = request.POST.get('name')
        referral_code = request.POST.get('referral_code')
        email = request.POST.get('email')
        channel_id = request.POST.get('channel_id')
        channel_secret = request.POST.get('channel_secret')
        access_token = request.POST.get('access_token')
        
        user = get_object_or_404(User, id=pk)
        if user.email == email:
            pass
        else:
            try:
                user = User.objects.get(email=email)
                print("同じメールを持つユーザーが既に存在します。")
                messages.add_message(request, messages.ERROR, '同じメールを持つユーザーが既に存在します。')            
            except User.DoesNotExist:
                pass
        if referral_code != '' or referral_code is not None:
            user.referral_code = referral_code 
        user.email = email        
         
        user.save()
        account = get_object_or_404(Account, user_id=user.id)
        if name != '' or name is not None:
            account.name = name        
        account.channel_id = channel_id
        account.channel_secret = channel_secret
        account.access_token = access_token
        account.save()
        
        messages.add_message(request, messages.SUCCESS, '成功。')
        return redirect(reverse("dashboard:usermanage"))
    except:
        print('failed!')
        messages.add_message(request, messages.ERROR, '失敗!') 
        return redirect(reverse("dashboard:usermanage"))

class AccountHistoryView(SuperUserCheck,ListView):
    model = Account
    paginate_by = 10
    template_name = 'user/account_history.html'
    
    def get_queryset(self):
        
        return Account.history.all()
    
@user_passes_test(lambda u: u.is_superuser)
def delete_account_history(request, history_id):    
    Account.history.filter(history_id=history_id).delete()  
    
    return redirect(reverse("dashboard:account-history"))
    
class ItemHistoryView(SuperUserCheck,ListView):
    model = Item
    paginate_by = 10
    template_name = 'user/item_history.html'
    
    def get_queryset(self):        
        return Item.history.all()

@user_passes_test(lambda u: u.is_superuser)
def delete_item_history(request, history_id):    
    Item.history.filter(history_id=history_id).delete()  
    
    return redirect(reverse("dashboard:item-history"))