from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('', views.store, name='store'),
                  path('cart/', views.cart, name='cart'),
                  path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
                  path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
                  path('checkout/<int:id>', views.checkout, name='checkout'),
                  path('product/', views.product, name='product'),
                  path('add_product/', views.add_product, name='add_product'),
                  path('order_item_change/<int:product_id>/<int:quantity>', views.order_item_change,
                       name='order_item_change'),
                  path('confirmation/', views.confirmation, name='confirmation'),
                  path('register/', views.register, name='register'),
                  path('login_page/', views.login_page, name='login_page'),
                  path('logout_user/', views.logout_user, name='logout_user'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
