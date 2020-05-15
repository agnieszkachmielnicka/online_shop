from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Category, Basket, ProductsList, ProductsInBasket, Order, Country
from main.forms import OrderForm


def index(request):

    if request.method == "POST":
        query = request.POST.get('search').lower()
        try:
            product_object = Product.objects.get(product_name__iexact=query)
            products_list = ProductsList.objects.filter(product=product_object).values_list('product', 'product_quantity')
        except Product.DoesNotExist:
            if query:
                messages.error(request, 'It seems to me that we do not have what you are looking for')
                return redirect('main:index')
            else:
                products_list = ProductsList.objects.values_list('product', 'product_quantity')
    else:
        products_list = ProductsList.objects.values_list('product', 'product_quantity')
    product_dict = {}
    for product in products_list:
        p, q = product
        prod = Product.objects.get(pk=p)
        product_dict[prod] = q

    context = {'products': product_dict,
                'search': True}

    return render(request, 'main/index.html', context)


def categories(request):

    if request.method == "POST":
        query = request.POST.get('search').lower()
        print(query)
        try:
            if query:
                categories_list = Category.objects.filter(category_name__iexact=query)
            else:
                categories_list = Category.objects.all()
        except Category.DoesNotExist:
            messages.error(request, 'It seems to me that we do not have what you are looking for')
            return redirect('main:category')
    else:
        categories_list = Category.objects.all()

    context = {'categories': categories_list,
                'search': True}
    return render(request, 'main/categories.html', context)


def single_category(request, category_name):
    category = Category.objects.get(category_name=category_name)
    products = category.products.all()
    avaiable_products = []
    for prod in products:
        print(prod)
        product_list = ProductsList.objects.get(product=prod)
        if product_list.product_quantity > 0:
            avaiable_products.append(prod)
    context = {'products': avaiable_products}
    return render(request, 'main/single_category.html', context)


@login_required()
def basket(request):
    if request.user.is_authenticated:
        user = request.user

    basket, created = Basket.objects.get_or_create(user=user)
    products_in_basket = ProductsInBasket.objects.filter(basket_id=basket)
    products_list = []
    if products_in_basket:
        products = products_in_basket.values_list('product_id', 'product_quantity')
        for product in products:
            p, q = product
            if q > 0:
                products_list.append((Product.objects.get(pk=p), q))
    context = {'products_list': products_list}
    return render(request, 'main/basket.html', context)


def add_product_to_basket(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    basket, created = Basket.objects.get_or_create(user=user)
    product_in_basket, created = ProductsInBasket.objects.get_or_create(basket_id=basket, product_id=product)
    product_in_basket.product_quantity = product_in_basket.product_quantity + 1
    product_in_basket.save()
    product_list = ProductsList.objects.get(product_id=product)
    product_list.product_quantity = product_list.product_quantity - 1
    product_list.save()
    return redirect('main:index')


def remove_product_from_basket(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    basket = Basket.objects.get(user=user)
    product_in_basket = ProductsInBasket.objects.get(basket_id=basket, product_id=product)
    if product_in_basket.product_quantity > 1:
        product_in_basket.product_quantity = product_in_basket.product_quantity - 1
        product_in_basket.save()
    else:
        product_in_basket.product_quantity = 0
        product_in_basket.delete()
    basket.save()
    product_list = ProductsList.objects.get(product_id=product)
    product_list.product_quantity = product_list.product_quantity + 1
    product_list.save()
    return redirect('main:basket')

def order(request):
    basket = Basket.objects.get(user=request.user)
    products_in_basket = ProductsInBasket.objects.filter(basket_id=basket)
    products = products_in_basket.values_list('product_id', 'product_quantity')
    products_list = []
    total = 0
    for product in products:
        p, q = product
        total_for_one = Product.objects.get(pk=p).product_price * q
        total = total + total_for_one
        products_list.append((Product.objects.get(pk=p), q, total_for_one))

    form = OrderForm()

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():
            order = Order(user=request.user, total_price=total, payment_method = form.cleaned_data['payment_method'], address=form.cleaned_data['address'], postal_code=form.cleaned_data['postal_code'], city=form.cleaned_data['city'], country=form.cleaned_data['country'])
            order.save()
            for product_tuple in products:
                product, quantity = product_tuple
                order.products.add(Product.objects.get(pk=product))
            order.save()
            clean_basket(products_in_basket)
            return redirect('thanks')

    context = {'products': products_list, 'total': total, 'form': form}

    return render(request, 'main/order.html', context)


def history(request):
    orders = Order.objects.filter(user=request.user).order_by('date_of_order')
    context = {'orders': list(orders)}
    return render(request, 'main/history.html', context)

def clean_basket(products_in_basket):
    for product_in_basket in products_in_basket:
        product_in_basket.delete()

def check_if_filled(request):
    pass
