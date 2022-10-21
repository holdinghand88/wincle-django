from django.urls import path
from . import views

app_name = "broadcast"

urlpatterns = [   
    path('', views.MessageView.as_view(), name='message-view'),    
    path('history-list', views.BroadcastHistoryListView.as_view(), name='broadcast-list'),
    path('history-delete/<int:pk>', views.delete_message, name='broadcast-delete'),
]