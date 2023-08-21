from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', views.product, name='product'),
    path('confirmation/', views.confirmation, name='confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)