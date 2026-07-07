from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<str:order_number>/', views.order_success, name='order_success'),
    path('add/<int:product_id>/', views.add, name='add'),
    path('remove/<int:product_id>/', views.remove, name='remove'),
    path('update/<int:product_id>/', views.update, name='update'),
]
