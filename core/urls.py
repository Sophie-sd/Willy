from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('promotions/', views.promotions, name='promotions'),
    path('delivery/', views.delivery, name='delivery'),
    path('faq/', views.faq, name='faq'),
    path('reviews/', views.reviews_redirect, name='reviews'),
    path('kontakty/', views.contacts, name='contacts'),
    path('contacts/', views.contacts_legacy_redirect),
    path('offer/', views.content_page, {'slug': 'offer'}, name='offer'),
    path('privacy/', views.content_page, {'slug': 'privacy'}, name='privacy'),
]
