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

class DashboardView(auth_views.LoginView):
    model = User
    template_name = 'dashboard.html'
    
    def get(self, request,*args,**kwargs):
        context = self.get_context_data()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return redirect("dashboard:usermanage")
            elif self.request.user.is_staff:
                return redirect("dashboard:dashboard-master")
            else:
                return render(request, self.template_name, context)
        else:
            return redirect("dashboard:account_login")        
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)

@login_required
def user_login(request,pk):
    user = get_object_or_404(User,id=pk)
    print(user)
    login(request, user)    
    return redirect(reverse("dashboard:dashboardview"))

