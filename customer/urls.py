from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [   
    path('list/', views.ListCustomerView.as_view(), name='customers-list'),
    path('create/', views.addnewuser, name='customer-create'),
    path('<str:customer_id>/update/', views.userinfoupdate, name='customer-update'),
    path('<str:customer_id>/delete/', views.DeleteCustomerView.as_view(), name='customer-delete'),
    path('<str:customer_id>/detail/', views.DetailCustomerView.as_view(), name='customer-detail'),
    path('avatar/', views.update_user_photo, name='update_user_photo'),
    path('inactive', views.inactive, name='inactive'),

    # Ajax Search Urls
    path('delete-checked', views.CustomerDeleteCheckedView.as_view(), name='customer-delete-checked'),
    path('customer-list-search/', views.CustomerNameDetailSearchView.as_view(), name='customer-list-search'),
    
    # Customer Filter
    path('filter_customer', views.filter_customer, name='filter_customer'),
]