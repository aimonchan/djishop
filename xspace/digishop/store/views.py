from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime
from .utils import cartData, guestOrder
from .forms import CreateUserForm, CustomAuthenticateForm, SearchForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

def searched_product(request):
    form = SearchForm(request.GET)  # Use GET to make it URL-friendly
    searchproducts = []

    if form.is_valid():
        searched = form.cleaned_data.get('searched')
        if searched:
            searchproducts = Product.objects.filter(name__icontains=searched)

    if request.headers.get('HX-Request'):  # Check if it's an HTMX request
        return render(request, 'store/partials/searched_product.html', {'searchproducts': searchproducts})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    try:
        customer = request.user.customer
    except:
        customer= None
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    data = cartData(request)
    cartItems = data['cartItems']
    # If it's an HTMX request, render a partial template showing the added product
    if request.headers.get('HX-Request'):
        return render(request, 'store/partials/cart_icon_update.html', {'product': product, 'action': action, 'customer':customer, 'cartItems':cartItems})
    # If it's not an HTMX request, redirect to a page or return full response
    return JsonResponse({'message': 'Product added to cart', 'cart': cart})

def cart_html_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    try:
        customer = request.user.customer
    except:
        customer= None
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    data = cartData(request)
    cartItems = data['cartItems']

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 
    # If it's an HTMX request, render a partial template showing the added product
    if request.headers.get('HX-Request'):
        return render(request, 'store/cart.html', {'items': items, 'order':order,'product': product, 'action': action, 'customer':customer, 'cartItems':cartItems})
    return render(request, 'store/cart.html',{'items': items, 'order':order,'product': product, 'action': action, 'customer':customer, 'cartItems':cartItems})


def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer=customer,complete=False)
    else:
        print('User is logged out')
        customer, order = guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id= transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order= order,
            address= data['shipping']['address'],
            city= data['shipping']['city'],
            state= data['shipping']['state'],
            zipcode= data['shipping']['zipcode'],
            )
    print('Data:', request.body)
    return JsonResponse('Payment complete..', safe=False)


# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     print('Action:', action)
#     print('ProductId:', productId)

#     customer = request.user.customer
#     product= Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

#     if action == 'add':
#         orderItem.quantity=(orderItem.quantity+1)
#     elif action == 'remove':
#         orderItem.quantity=(orderItem.quantity-1)
#     orderItem.save()
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#     data = cartData(request)
#     cartItems = data['cartItems']
#     context = {'cartItems':cartItems}
#     if request.headers.get('HX-Request'):
#            # If it's an HTMX request, return only the part of the page to update
#           return render(request, 'store/partials/cart_icon_update.html', context)
#     return JsonResponse('Item was added', safe= False)


def updateItem(request):
    if request.method == "POST":
        try:
            # Make sure you're getting the correct JSON payload from the request body
            data = json.loads(request.body)

            # Debugging: log the data you're receiving
            print("Received data:", data)

            # Extract the parameters you need
            product_id = data.get('productId')
            action = data.get('action')

            # Simple validation for required fields
            if not product_id or not action:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Do something with the data (e.g., update the cart)
            # Example: update_cart(product_id, action)

            return JsonResponse({"status": "success"})

        except json.JSONDecodeError:
            # If the JSON is malformed
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            # Catch any other unexpected errors
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



# Create your views here.
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()

    # set up pagination
    p = Paginator(Product.objects.all(),12)
    page = request.GET.get('page')
    productPagis = p.get_page(page)
    nums = "a" * productPagis.paginator.num_pages
    context = {'products': products, 'cartItems':cartItems,'items': items, 'order':order, 'nums':nums,'productPagis':productPagis}
    if request.headers.get('HX-Request'):
           # If it's an HTMX request, return only the part of the page to update
          return render(request, 'store/partials/item_list_content.html', context)
    
    return render(request, 'store/home.html', context)

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    
    context ={'form': form}
    return render(request, 'store/signup.html',context)

def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = CustomAuthenticateForm(request, data= request.POST)
        if form.is_valid():
            user= form.get_user()
            login(request, user)
            email=user.email
            username=user.username
            try:
                user = User.objects.get(username=username)
                customer, created= Customer.objects.get_or_create(user=user,name=username,email=email)
            except:
                messages.error(request, 'Username does not exist')
        return redirect('home')

    context={'form':form}
    return render(request, 'store/signin.html',context)

def signout(request):
    logout(request)
    return redirect('signin')

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']    
    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html',context)

def wishlist(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    context={}
    return render(request, 'store/wishlist.html',context)

def account(request):
    return render(request, 'store/account.html')

def ourstory(request):
    return render(request, 'store/ourstory.html')

def contact(request):
    return render(request, 'store/contact.html')


def productdetail(request, product_id):
    # Get the product by its ID, or return a 404 error if not found
    product = get_object_or_404(Product, pk=product_id)
    # Render the product detail template with the product context
    return render(request, 'store/productdetail.html', {'product': product})


def notfound(request):
    return render(request, 'store/404.html')

def test(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()

    p = Paginator(Product.objects.all(),12)
    page = request.GET.get('page')
    productPagis = p.get_page(page)
    nums = "a" * productPagis.paginator.num_pages


    context = {'products': products, 'cartItems':cartItems,'items': items, 'order':order, 'nums':nums,'productPagis':productPagis}
    return render(request, 'store/testtemplates/test.html',context)

def testtwo(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()

    p = Paginator(Product.objects.all(),12)
    page = request.GET.get('page')
    productPagis = p.get_page(page)
    nums = "a" * productPagis.paginator.num_pages


    context = {'products': products, 'cartItems':cartItems,'items': items, 'order':order, 'nums':nums,'productPagis':productPagis}
    
    if request.headers.get('HX-Request'):
           # If it's an HTMX request, return only the part of the page to update
          return render(request, 'store/partials/item_list_content.html', context)
    
       
    return render(request, 'store/testtemplates/testtwo.html',context)
