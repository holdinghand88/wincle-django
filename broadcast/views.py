from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse, get_object_or_404,HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.db.models import Q

from customer.models import Customer
from .models import BroadcastHistory

################## メッセージ配信 ###################
class MessageView(LoginRequiredMixin,TemplateView):
    template_name = 'talk/message.html'
    
    def get(self,request):
        context = self.get_context_data()
        
        return render(request, self.template_name,context)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        broadcast = BroadcastHistory.objects.filter(user=self.request.user)
        amount = len(broadcast)
        limit = 1000
        context['amount'] = amount
        context['limit'] = limit
        context['rate'] = (amount/1000)*100
        context['range'] = range(5)
        return context
    
    def post(self,request):
        context = self.get_context_data()
        is_all = request.POST.get("is_all")
        if is_all == '0':
            target = '絞り込む'
            name = request.POST.get("name")
            line_name = request.POST.get("line_name")
            tel = request.POST.get("tel")
            tags = request.POST.get("tags")
            q = Q()
            if name or line_name or tel or tags:
                if name:
                    q &= Q(name__icontains=name)
                if line_name:
                    q &= Q(line_name__exact=line_name)
                if tel:
                    q &= Q(tel__exact=tel)
                if tags:
                    q &= Q(tags__exact=tags)
                    
                customers = Customer.objects.filter(q).filter(account_id=request.user.account.id)
            else:
                customers = Customer.objects.filter(account_id=request.user.account.id)
        else:
            target = 'すべての友だち'
            customers = Customer.objects.filter(account_id=request.user.account.id)
        print(customers)
        message_types0 = request.POST.get("message_types[0][]")
        message_types1 = request.POST.get("message_types[1][]")
        message_types2 = request.POST.get("message_types[2][]")
        message_types3 = request.POST.get("message_types[3][]")
        message_types4 = request.POST.get("message_types[4][]")        
        
        contents0 = request.POST.get("contents[0]")
        contents1 = request.POST.get("contents[1]")
        contents2 = request.POST.get("contents[2]")
        contents3 = request.POST.get("contents[3]")
        contents4 = request.POST.get("contents[4]")
        file_url = ''    
        
        print(contents0)
        if message_types0 == 'image':
            file_url = request.POST.get("images[0]")
            
        if message_types0 == 'videos':
            file_url = request.POST.get("videos[0][0]")
            videos0_1 = request.POST.get("videos[0][1]")
        print(file_url)
                  
        broadcast = BroadcastHistory()
        broadcast.user = request.user
        broadcast.content = contents0
        broadcast.file_url = file_url
        broadcast.target = target
        broadcast.save()
        for customer in customers: 
            broadcast.customer.add(customer)
        
        return render(request, self.template_name,context)
    
class BroadcastHistoryListView(LoginRequiredMixin,ListView):
    template_name = 'talk/broadcast_history.html'
    model = BroadcastHistory
    paginate_by = 10
    
    def get_queryset(self):
        return BroadcastHistory.objects.filter(user=self.request.user).order_by('-created_at')
    

def delete_message(request,pk):
    obj = get_object_or_404(BroadcastHistory, id=pk)
    obj.delete()
    return redirect("broadcast:broadcast-list")