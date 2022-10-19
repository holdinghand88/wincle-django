from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from ..models import User,Account
from ..permissions import SuperUserCheck,StaffUserCheck
   
class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'user/user_detail.html'
    
@login_required
def update_account_info(request,pk):
    try:
        account = Account.objects.get(user_id=pk)
        account.name = request.POST.get('name')
        account.description = request.POST.get('description')
        account.notify_token = request.POST.get('notify_token')
        account.address = request.POST.get('address')
        account.instagram_id = request.POST.get('instagram_id')
        account.line_url = request.POST.get('line_url')
        account.deadline_day = request.POST.get('deadline_day')
        account.save()
        if 'avatar' in request.FILES:
            avatar = request.FILES.get('avatar')
            account.avatar = avatar
            account.save()
        messages.add_message(request, messages.SUCCESS, '成功的に変更されました。')
        return redirect('dashboard:user-detail', pk=pk)
    except:
        messages.add_message(request, messages.ERROR, '失敗!')
        return redirect('dashboard:user-detail', pk=pk)
    
@login_required
def update_salesetting_info(request,pk):
    try:
        account = Account.objects.get(user_id=pk)        
        account.reduction_rate = request.POST.get('reduction_rate')
        account.bank_info = request.POST.get('bank_info')
        account.pay_channel_id = request.POST.get('pay_channel_id')
        account.pay_channel_secret = request.POST.get('pay_channel_secret')
        account.postage = request.POST.get('postage')
        account.postage_free_border = request.POST.get('postage_free_border')
        account.save()
        
        messages.add_message(request, messages.SUCCESS, '成功的に変更されました。')
        return redirect('dashboard:user-detail', pk=pk)
    except:
        messages.add_message(request, messages.ERROR, '失敗!')
        return redirect('dashboard:user-detail', pk=pk)
    
