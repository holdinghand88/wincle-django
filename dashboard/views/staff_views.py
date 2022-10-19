from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from ..models import User,Account
from ..forms import AddUserCreateForm,AddChildUserCreateForm
from ..permissions import SuperUserCheck,StaffUserCheck
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm

class MasterDashboardView(StaffUserCheck,TemplateView):
    model = User
    template_name = 'dashboard-master.html'
    
class MasterUserManageView(StaffUserCheck,ListView):
    model = User
    paginate_by = 10
    template_name = 'user/child-userlist.html'
    
    def get_queryset(self, **kwargs):
        return User.objects.filter(referral_code=self.request.user.referral_code).exclude(is_staff=True).order_by('-id')
  
@login_required
def childuserinfoupdate(request,pk):
    try:        
        name = request.POST.get('name')        
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
        user.email = email
        user.save()
        account = get_object_or_404(Account, user_id=user.id)
        
        account.name = name        
        account.channel_id = channel_id
        account.channel_secret = channel_secret
        account.access_token = access_token
        account.save()
        
        messages.add_message(request, messages.SUCCESS, '成功。')
        return redirect(reverse("dashboard:childusermanage"))
    except:
        print('failed!')
        messages.add_message(request, messages.ERROR, '失敗!') 
        return redirect(reverse("dashboard:childusermanage"))

