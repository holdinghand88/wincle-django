from django.urls import path
from . import views

app_name = "talk"

urlpatterns = [   
    path('', views.TalkView.as_view(), name='talkview'),
    path('<str:customer_id>', views.TalkDetail.as_view(), name='talk-detail'),
]