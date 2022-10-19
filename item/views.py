from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse, get_object_or_404,HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from item.models import Item,ItemCategory,Order,OrderItem
from django.http import JsonResponse
from django.db.models import Q

@login_required
def add_category(request):
    try:
        name = request.POST.get('name')
        obj = ItemCategory.objects.filter(account_id=request.user.account.id).filter(name=name)
        print(name)
        if len(obj) > 0:
            print("同じカテゴリー名が既に存在します。")
            return JsonResponse({'Failed':'同じカテゴリー名が既に存在します。'})            
        else:
            pass        
        obj = ItemCategory.objects.create(account_id=request.user.account.id,name=name)        
        return JsonResponse({'obj_id':obj.id})
    except:        
        return JsonResponse({'Failed':True})

@login_required   
def delete_category(request):
    pk = request.POST.get('id')
    obj = get_object_or_404(ItemCategory, id=pk)
    obj.delete()
    return JsonResponse({'success':True})

class ListItemView(ListView):
    model = Item
    template_name = 'item/item_list.html'
    context_object_name = 'items'    

    def get_queryset(self):
        search_key = self.request.GET.get('searchfield')
        queryset = Item.objects.filter(account_id=self.request.user.account.id).order_by('-created_at')
        if search_key == '' or search_key is None:
            items_list = queryset
            self.request.session['search_key'] = ''
        else:
            items_list = queryset.filter(name__icontains=search_key)
            self.request.session['search_key'] = search_key
        
        return items_list

class InfiniteScrollItem(TemplateView):
    def get(self, request, *args, **kwargs):
        limit = int(self.request.GET.get('limit'))
        page = self.request.GET.get('page')
        available_item = self.request.GET.get('available_item')
        search_key = self.request.GET.get('search_key')
        print(search_key)
        queryset = Item.objects.filter(account_id=self.request.user.account.id).order_by('-created_at')
        if search_key == '' or search_key is None:
            items_list = queryset
        else:
            items_list = queryset.filter(name__icontains=search_key)
            print(items_list)
        start = 0
        if page == '1':
            start = 0
            limit = 8
        else:
            start = int(available_item)
            
        
        items = items_list[start:start+limit]        
        
        html = render_to_string("item/item_scroll_infinite.html",{'items':items,'start':start},request=request)
        return JsonResponse({'status':'success','html':html,'total_items': len(items)})
    
class ItemDetailView(LoginRequiredMixin,DetailView):
    model = Item
    template_name = 'item/item_detail.html'
    
    def post(self,request,pk):
        try:            
            obj = Item.objects.get(id=pk)
            obj.name = request.POST.get('name')      
            if request.POST.get('price'):
                obj.price = request.POST.get('price')
            if request.POST.get('sale_price'):
                obj.sale_price = request.POST.get('sale_price')
            if request.POST.get('discount_price'):
                obj.discount_price = request.POST.get('discount_price')
            if request.POST.get('sale_sdate'):
                obj.sale_sdate = request.POST.get('sale_sdate')
            if request.POST.get('sale_edate'):
                obj.sale_edate = request.POST.get('sale_edate')
            if request.POST.get('category'):
                obj.category_id = request.POST.get('category')
            if request.POST.get('max_point'):
                obj.max_point = request.POST.get('max_point')
            if request.POST.get('quantity'):
                obj.quantity = request.POST.get('quantity')
            if request.POST.get('order_max_quantity'):
                obj.order_max_quantity = request.POST.get('order_max_quantity')
            
            if 'image1' in request.FILES:
                image1 = request.FILES.get('image1')
                obj.image1 = image1
            print(obj)
            obj.save()
            messages.add_message(request, messages.SUCCESS, '成功。')
            return redirect("item:item-detail",pk=pk)
        except:
            messages.add_message(request, messages.ERROR, '失敗!') 
            return redirect("item:item-detail",pk=pk)
    
class ItemCreateView(LoginRequiredMixin,CreateView):
    model = Item
    template_name = 'item/item_create.html'
    
    def get(self,request):
        return render(request, self.template_name)

    def post(self,request):
        try:
            obj = Item()
            obj.account = request.user.account
            obj.name = request.POST.get('name')
            if request.POST.get('price'):
                obj.price = request.POST.get('price')
            if request.POST.get('sale_price'):
                obj.sale_price = request.POST.get('sale_price')
            if request.POST.get('discount_price'):
                obj.discount_price = request.POST.get('discount_price')
            if request.POST.get('sale_sdate'):
                obj.sale_sdate = request.POST.get('sale_sdate')
            if request.POST.get('sale_edate'):
                obj.sale_edate = request.POST.get('sale_edate')
            if request.POST.get('category'):
                obj.category_id = request.POST.get('category')
            if request.POST.get('max_point'):
                obj.max_point = request.POST.get('max_point')
            if request.POST.get('quantity'):
                obj.quantity = request.POST.get('quantity')
            if request.POST.get('order_max_quantity'):
                obj.order_max_quantity = request.POST.get('order_max_quantity')
            
            if 'image1' in request.FILES:
                image1 = request.FILES.get('image1')
                obj.image1 = image1
            
            obj.save()
            messages.add_message(request, messages.SUCCESS, '成功。')
            return redirect("item:item-list")
        except:
            messages.add_message(request, messages.ERROR, '失敗!') 
            return redirect("item:item-list")
        
@login_required   
def delete_item(request,pk):    
    obj = get_object_or_404(Item, id=pk)
    obj.delete()
    return redirect("item:item-list")

############### 商品販売履歴  ############################
class SaleHistoryListView(LoginRequiredMixin,ListView):
    model = Order
    #paginate_by = 10
    template_name = 'item/salehistory_list.html'
    
    def get_queryset(self, *args, **kwargs):        
        return Order.objects.all().order_by('-id')

class SaleHistoryInfiniteScroll(View):
    def get(self, request, *args, **kwargs):
        limit = int(self.request.GET.get('limit'))
        page = self.request.GET.get('page')
        available_item = self.request.GET.get('available_item')
        items_list = Order.objects.all().order_by('-id')
        
        # Detail Search
        detailNameInput = self.request.GET.get('detailNameInput', None)
        detailLineInput = self.request.GET.get('detailLineInput', None)
        if detailNameInput is not None:
            items_list = items_list.filter(customer__name__icontains=detailNameInput)
        
        
            
        start = 1
        if page == '1':
            start = 0
        else:
            start = int(available_item)
        #print(start)
        items = items_list[start:start+limit]
        html = render_to_string("item/salehistory_scroll_infinite.html",{'items':items,'start':start},request=request)
        return JsonResponse({'status':'success','html':html,'total_items': len(items)})

@login_required   
def delete_order(request,pk):    
    obj = get_object_or_404(Order, id=pk)
    obj.delete()
    return redirect("item:salehistory_list")

class SaleDetailView(LoginRequiredMixin,DetailView):
    model = Item
    template_name = 'item/sale_detail.html'
