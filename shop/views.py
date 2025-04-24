#from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.http import Http404

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
        price = request.POST['price']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        
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

# Widok zestawienia zamówień za dany miesiąc
def order_summary(request, year, month):
    orders = Order.objects.filter(date__year=year, date__month=month)
    return render(request, 'shop/order_summary.html', {'orders': orders})

# Create your views here.
