from django.urls import path
from . import views

app_name = "item"

urlpatterns = [   
    path('list/', views.ListItemView.as_view(), name='item-list'),
    path("infinitescroll/", views.InfiniteScrollItem.as_view(), name="infinitescroll"),
    
    path('new/', views.ItemCreateView.as_view(), name='item-create'),
    path('detail/<str:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    #path('update/<int:pk>', views.groupinfoupdate, name='groupupdate'),
    path('delete/<str:pk>', views.delete_item, name='itemdelete'),
    
    #商品カテゴリー
    path('category/add', views.add_category, name='add_category'),
    path('category/delete', views.delete_category, name='delete_category'),
    
    #商品販売履歴
    path('sale-history', views.SaleHistoryListView.as_view(), name='sale-history'),
    path('sale-detail/<str:pk>', views.SaleDetailView.as_view(), name='sale-detail'),
    path('sale-history/infinite', views.SaleHistoryInfiniteScroll.as_view(), name='sale-history-infinite'),
    path('sale-history/<str:pk>', views.delete_order, name='delete_sale'),
]