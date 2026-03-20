from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def root_dashboard(request):
    return render(request, 'dashboard.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_dashboard, name='dashboard'),
    path('catalog/', include('catalog.urls')),
    path('sales/', include('sales.urls')),
    path('promotions/', include('promotions.urls')),
    path('identity/', include('identity.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
