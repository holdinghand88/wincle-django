from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('accounts/', include(('accounts.urls', 'accounts'),namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),   
    path('customer/', include('customer.urls',namespace='customer')),
    path('item/', include('item.urls',namespace='item')),
    path('talk/', include('talk.urls',namespace='talk')),
    path('broadcast/', include('broadcast.urls',namespace='broadcast')),
]

if not settings.PRODUCTION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)