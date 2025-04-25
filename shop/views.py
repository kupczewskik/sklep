from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.http import require_POST

# Widok listy produktów
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# Widok szczegółów produktu
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

# Widok edycji produktu
def product_edit(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
    else:
        product = Product()

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price'].replace(',', '.')
        category_id = request.POST['category']
        category = get_object_or_404(Category, id=category_id)

        product.name = name
        product.description = description
        product.price = price
        product.category = category
        product.save()
        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'shop/product_edit.html', {'product': product, 'categories': categories})

# Widok usunięcia produktu
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('product_list')

# Widok kategorii produktów
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

# Widok kategorii produktów z aktywnymi linkami
def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/products_by_category.html', {
        'category': category,
        'products': products
    })

# Widok zestawienia zamówień za dany miesiąc
def order_summary(request, year, month):
    orders = Order.objects.filter(date__year=year, date__month=month)
    return render(request, 'shop/order_summary.html', {'orders': orders})

# Widok sklepu
def shop_view(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})

# Widok koszyka
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total,
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')

# Modyfikacja koszyka
@require_POST
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)

    request.session['cart'] = cart
    return redirect('cart_view')


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart_view')