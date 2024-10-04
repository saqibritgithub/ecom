from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

from .models import Category, Product, Review, Order,  Cart
from .forms import ReviewForm, OrderForm, CustomUserCreationForm



def home(request):
    categories = Category.objects.filter(parent_category__isnull=True)
    return render(request, 'store/home.html', {'categories': categories})

def category_detail(request, category_id):
    
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    products = Product.objects.filter(category=category)

    return render(request, 'store/category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'products': products
    })

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)
    products = Product.objects.filter(category=subcategory)
    
    return render(request, 'store/subcategory_detail.html', {
        'subcategory': subcategory,
        'products': products
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    is_logged_in = request.user.is_authenticated

    if request.method == 'POST':
        if 'order_submit' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.product = product
                 # Allow guest users to place orders
                order.save()
                return redirect('order_list')
        elif 'review_submit' in request.POST:
            if not is_logged_in:
                return HttpResponseForbidden("You must be logged in to submit a review.")
            
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('product_detail', product_id=product.id)
    else:
        order_form = OrderForm()  # Always show order form, even for guests
        review_form = ReviewForm() if is_logged_in else None

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'order_form': order_form,
        'review_form': review_form,
        'is_logged_in': is_logged_in,
    })
@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'store/review_edit.html', {'form': form, 'review': review})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == 'POST':
        review.delete()
        return redirect('product_detail', product_id=review.product.id)

    return render(request, 'store/review_delete.html', {'review': review})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=None)
    for order in orders:
        order.total_price = order.product.price * order.quantity
    return render(request, 'store/order_list.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login or any other page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'store/register.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        cart.save()
        return redirect('product_detail', product_id=product_id)
    else:
        return redirect('login')

@login_required
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    total_bill = sum(product.price for product in products)
    
    return render(request, 'store/cart.html', {'products': products, 'total_bill': total_bill})



