from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse, get_object_or_404,HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.db.models import Q

from customer.models import Customer
from .models import Talk

class TalkView(LoginRequiredMixin,TemplateView):
    model = Talk    
    template_name = 'talk/talk.html'
    
    def get(self,request):
        queryset = Talk.objects.filter(account=request.user.account)
        customer_ids = Talk.objects.filter(account=request.user.account).values_list('customer', flat=True).distinct()
        
        context = {}
        context['customer_ids'] = customer_ids
        
        if request.POST.get('customer_id'):
            customer_id = request.POST.get('customer_id')
            context['selected_chatter'] = customer_id
            talks = queryset.filter(customer_id=customer_id).order_by('created_at')
        else:
            selected_chatter = customer_ids[0]
            context['selected_chatter'] = selected_chatter
            talks = queryset.filter(customer_id=customer_ids[0]).order_by('created_at')
        print(talks)
        context['talks'] = talks
        return render(request, self.template_name, context)
    
class TalkDetail(LoginRequiredMixin,TemplateView):
    model = Talk    
    template_name = 'talk/talk.html'
    
    def get(self,request,customer_id):
        queryset = Talk.objects.filter(account=request.user.account)
        customer_ids = Talk.objects.filter(account=request.user.account).values_list('customer', flat=True).distinct()
        context = {}
        context['customer_ids'] = customer_ids        
        
        context['selected_chatter'] = customer_id
        talks = queryset.filter(customer_id=customer_id).order_by('created_at')
        
        context['talks'] = talks
        return render(request, self.template_name, context)
        
        