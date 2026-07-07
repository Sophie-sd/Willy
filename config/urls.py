import datetime

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.http import require_GET

from catalog import views as catalog_views


@require_GET
def healthz(request):
    return JsonResponse({'status': 'ok', 'timestamp': datetime.datetime.now().isoformat()})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', healthz, name='healthz'),
    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('search/', catalog_views.search, name='search'),
    path('product/<slug:slug>/', catalog_views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', catalog_views.category_detail, name='category'),
    path(
        '<slug:category_slug>/<slug:subcategory_slug>/',
        catalog_views.subcategory_detail,
        name='subcategory',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
