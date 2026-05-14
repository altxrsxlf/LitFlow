from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Category, Order
from .cart import Cart

def home(request):
    books = Book.objects.filter(available=True)[:8]
    return render(request, 'core/home.html', {'books': books})

def catalog(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    books = Book.objects.filter(available=True)
    if category_slug:
        books = books.filter(category__slug=category_slug)
    return render(request, 'core/catalog.html', {'books': books, 'categories': categories})

def book_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug, available=True)
    return render(request, 'core/book_detail.html', {'book': book})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'core/cart_detail.html', {'cart': cart})

def cart_add(request, id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=id)
    cart.add(book=book)
    return redirect('core:cart_detail')

def cart_remove(request, id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=id)
    cart.remove(book)
    return redirect('core:cart_detail')

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city')
        )
        for item in cart:
            order.items.create(book=item['book'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return render(request, 'core/order_success.html', {'order': order})
    return render(request, 'core/order_create.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_history.html', {'orders': orders})

@login_required
def profile(request):
    return render(request, 'core/profile.html')

def search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(available=True, title__icontains=query) if query else []
    return render(request, 'core/search.html', {'books': books, 'query': query})

def about(request):
    return render(request, 'core/about.html')