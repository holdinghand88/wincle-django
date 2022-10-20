from django.urls import path
from dashboard.views import user_views,home_views,admin_views,staff_views
from allauth.account.views import LogoutView,LoginView 

app_name = 'dashboard'

urlpatterns = [
    ## ユーザー管理
    path('', home_views.DashboardView.as_view(), name='dashboardview'),
    path('login', LoginView.as_view(), name='account_login'),
    path('logout', LogoutView.as_view(), name='account_logout'),
    path('master', staff_views.MasterDashboardView.as_view(), name='dashboard-master'),
    path('user-list', admin_views.UserManageView.as_view(), name='usermanage'),
    path('childuser-list', staff_views.MasterUserManageView.as_view(), name='childusermanage'),
    path('user/add', admin_views.addnewuser, name='useradd'),
    path('user-child/addnewuser', admin_views.childaddnewuser, name='childuseradd'),
    path('user/update/<str:pk>', admin_views.userinfoupdate, name='userupdate'),
    path('user-child/update/<str:pk>', staff_views.childuserinfoupdate, name='childuserupdate'),
    path('user/inactive', admin_views.inactive, name='inactive'),
    path('user/delete/<str:pk>', admin_views.deletuser, name='userdelete'),
    path('user/login/<str:pk>', home_views.user_login, name='user-login'),
    
    path('account-detail/<str:pk>', user_views.UserDetailView.as_view(), name='user-detail'),
    path('account-info-update/<str:pk>', user_views.update_account_info, name='account-info-update'),
    path('salesetting-info-update/<str:pk>', user_views.update_salesetting_info, name='salesetting-info-update'),
    
    ##履歴
    path('account-history', admin_views.AccountHistoryView.as_view(), name='account-history'),
    path('account-history/delete/<int:history_id>', admin_views.delete_account_history, name='delete_account_history'),
    path('item-history', admin_views.ItemHistoryView.as_view(), name='item-history'),
    path('item-history/delete/<int:history_id>', admin_views.delete_item_history, name='delete_item_history'),
]
