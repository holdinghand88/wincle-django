from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404,HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from customer.models import Customer
from django.http import JsonResponse
from customer.forms import CustomerForm,AddCustomerCreateForm
from django.db.models import Q


class ListCustomerView(ListView):
    model = Customer
    template_name = 'customer/list_customers.html'
    context_object_name = 'customers'
    paginate_by = 0

    def get_queryset(self):
        customers = Customer.objects.filter(account_id=self.request.user.account.id).order_by('-date_joined')
        return customers

def addnewuser(request):
    form = AddCustomerCreateForm(request.POST)
    
    if form.is_valid():
        customer = form.save()
        return redirect(reverse("customer:customers-list"))
    else:
        print("failed")
        return redirect(reverse("customer:customers-list"))

class DeleteCustomerView(DeleteView):
    model = Customer
    pk_url_kwarg = 'customer_id'
    template_name = 'customer/delete_customer.html'
    context_object_name = 'customer'

    def get_success_url(self):
        return reverse('customer:customers-list')


class DetailCustomerView(DetailView):
    model = Customer
    pk_url_kwarg = 'customer_id'
    template_name = "customer/customer_detail.html"
    context_object_name = 'customer'
    
def userinfoupdate(request,customer_id):
    form_class = CustomerForm(data=request.POST,pk=customer_id)
    if form_class.is_valid():
        try:
            user = form_class.update(customer_id)
            messages.add_message(request, messages.SUCCESS, '成功!')
            return redirect('customer:customer-detail', customer_id=customer_id)
        except:
            messages.add_message(request, messages.ERROR, '失敗!')
            return redirect('customer:customer-detail', customer_id=customer_id)        
    else:
        print("failed")
        messages.add_message(request, messages.ERROR, '失敗!')
        return redirect('customer:customer-detail', customer_id=customer_id)
    
def update_user_photo(request):
    pk = request.POST.get('id')
    customer = get_object_or_404(Customer,id=pk)
    if 'user_avatar' in request.FILES:
        avatar = request.FILES.get('user_avatar')
        customer.avatar = avatar
        customer.save()
        return JsonResponse({'success':True})
    
def inactive(request):
    pk = request.POST.get('customer_id')
    customer = get_object_or_404(Customer, id=pk)
    active_status = customer.is_leave
    if active_status:
        active_status = 0
    else:
        active_status = 1
    customer.is_leave = active_status
    customer.save()
    resp = HttpResponse(f'{{"active_status": "{customer.is_leave}"}}')
    resp.content_type = "application/json"
    resp.status_code = 200
    return resp


class CustomerNameDetailSearchView(View):
    def get(self, request):
        c = Customer.objects.all().count()
        print('users c', c)
        # name search
        # limit
        search_str = request.GET.get('searchText')
        page_no = request.GET.get('page_no')

        # offset = (page_no - 1) * limit
        # Detail
        name = request.GET.get('name')
        birthday = request.GET.get('birthday')        
        gender = request.GET.get('gender')
        point = request.GET.get('point')

        # Detail Search
        q = Q()

        if name or birthday or gender or point:
            if name:
                q &= Q(name__icontains=name)
            if birthday:
                q &= Q(birthday__exact=birthday)                
            if gender:
                q &= Q(gender__exact=gender)                
            if point:
                q &= Q(point__exact=point)

            customers = Customer.objects.filter(q).filter(account_id=self.request.user.account.id)

        elif search_str:
            customers_obj = Customer.objects.all()
            customers = customers_obj.filter(
                Q(name__icontains=search_str) & Q(account_id=self.request.user.account.id))
        else:
            customers = Customer.objects.filter(account_id=self.request.user.account.id)

        # paginator = Paginator(customers, 5)
        #
        limit = 10
        offset = (int(page_no) - 1) * limit
        new_customers = customers[offset:offset + limit]
        print("new_customers", new_customers)
        
        customer_list_arr = []
        for customer in new_customers:
            if customer.gender == 1:
                gender = '男性'
            else:
                gender = '女性'
            customer_list_obj = {}
            if customer.avatar:
                customer_list_obj['avatar'] = customer.avatar.url
            else:
                customer_list_obj['avatar'] = ''
            customer_list_obj['name'] = customer.name
            customer_list_obj['gender'] = gender
            customer_list_obj['birthday'] = customer.birthday
            customer_list_obj['point'] = customer.point
            customer_list_obj['tags'] = customer.tags
            customer_list_obj['active'] = customer.account.user.is_active
            customer_list_obj['id'] = customer.id            
            customer_list_arr.append(customer_list_obj)
        return JsonResponse({'customers': customer_list_arr, })


class CustomerDeleteCheckedView(View):
    def post(self, request):        
        checked_ids = request.POST.getlist('checked_ids[]')
        print('checked_ids', checked_ids)
        for id in checked_ids:
            Customer.objects.get(id=id).delete()
        return JsonResponse({})


def filter_customer(request):
    name = request.POST.get('name')
    line_name = request.POST.get('line_name')
    tel = request.POST.get('tel')
    tags = request.POST.get('tags')
    
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
    print(customers)
    return JsonResponse({'customers': len(customers)})