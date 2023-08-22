from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm
from .models import Product, ShopUser, Order, OrderItem
from django.contrib.auth.models import Group
from django.contrib import messages


# Create your views here.

def store(request):
    if request.method == "POST":
        return product(request, product_id=request.POST['product_id'])
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'store/store.html', context)


def cart(request):
    shop_user = ShopUser.objects.get(user=request.user)
    order, created = Order.objects.get_or_create(buyer=shop_user, is_ordered=False)

    order_items = order.orderitem_set.all()
    context = {"order": order, 'order_items': order_items}
    return render(request, 'store/cart.html', context)


def checkout(request, id):
    if request.method == "POST":
        order = Order(pk=id)
        order.is_ordered = True
        order.save()
        return redirect('confirmation')
    else:
        order = Order(pk=id)
    context = {"order": order}
    return render(request, "store/checkout.html", context=context)


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, 'store/product.html', context)


def order_item_change(request, product_id, quantity):
    order_item = OrderItem.objects.get(id=product_id)

    if request.method == "POST":
        order_item.quantity = request.POST['quantity']
        order_item.save()
        return redirect("cart")

    context = {"product": order_item, "quantity": quantity}
    return render(request, 'store/order_item_change.html', context)


def confirmation(request):
    context = {}
    return render(request, 'store/confirmation.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        shop_user = ShopUser.objects.get(user=request.user)
        print(shop_user)
        order, created = Order.objects.get_or_create(buyer=shop_user, is_ordered=False)
        product_id = request.POST.get('product_id')

        quantity = 1

        if not request.POST.get('quantity') == '':
            quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, pk=product_id)

        order_item_exists = order.orderitem_set.filter(product=product).first()

        if order_item_exists:
            order_item = order_item_exists
            order_item.quantity += quantity
            order_item.save()
        else:
            order_item = OrderItem.objects.create(product=product, order=order, quantity=quantity)
            order_item.save()

        print(order)

        return redirect('cart')
    # print(quantity)
    return redirect('store')


def delete_item(request, item_id=0):
    order_item = OrderItem.objects.get(pk=item_id)
    order_item.delete()
    return redirect('cart')


def register(request):
    form = CreateUserForm()
    shop_user = ShopUser()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='shop_user')
            user.groups.add(group)
            user.is_staff = True
            shop_user.user = user
            shop_user.username = user.username
            user.first_name = user.username
            shop_user.email = user.email
            user.save()
            shop_user.save()

            messages.add_message(request, messages.SUCCESS, 'Account was created for ' + user.username)
            return redirect('login_page')

    context = {"form": form}
    return render(request, "registration/register.html", context=context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.add_message(request, messages.ERROR, 'Bad credentials')

    context = {}
    return render(request, "registration/login.html", context=context)

#
# def product_list(request):
#     return
#
#
# def product_form(request):
#     return
#
#
# def product_delete(request):
#     return
