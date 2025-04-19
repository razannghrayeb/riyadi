from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      path("Shop_Main/",views.Shop_Main, name="Shop_Main"),
      path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
      path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
      path('cart/', views.cart, name='cart'),
      path('checkout/', views.checkout, name='checkout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
