from django.urls import path

from . import views
from orders import np_views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/np/cities/', np_views.np_cities, name='np_cities'),
    path('api/np/warehouses/', np_views.np_warehouses, name='np_warehouses'),
    path('api/np/streets/', np_views.np_streets, name='np_streets'),
    path('success/<str:order_number>/', views.order_success, name='order_success'),
    path('add/<int:product_id>/', views.add, name='add'),
    path('remove/<int:product_id>/', views.remove, name='remove'),
    path('update/<int:product_id>/', views.update, name='update'),
]
