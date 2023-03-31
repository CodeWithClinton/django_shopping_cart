from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.http import JsonResponse
import json
from django.contrib import messages
import uuid
from django.contrib.auth import authenticate, login


# Create your views here.


def index(request):
    products = Product.objects.all()
    
    # if request.user.is_authenticated:
    #     cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        
    context = {"products":products}
    return render(request, "index.html", context)


def cart(request):
    
    # cart = None
    # cartitems = []
    
    # cartitems = cart.cartitems.all()
    
    # if request.user.is_authenticated:
    #     cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    #     cartitems = cart.cartitems.all()
    
    # context = {"cart":cart}
    return render(request, "cart.html")

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        num_of_item = cart.num_of_items
        
    else:
        
        try:
            cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
            cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_items
            
        
        except:
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)
            cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_items
        
    
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)


def sign_in(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            print(request.user.username)
            
            try:
                cart = Cart.objects.get(session_id = request.session["nonuser"], completed=False)
                if Cart.objects.filter(user=request.user, completed=False).exists():
                    cart.user = None
                    cart.save()
                
                else:
                    cart.user = request.user
                    cart.save()
                
            
            except:
                print("omooooooooooo")
                
            # try:
                
            #     cart = Cart.objects.get(session_id = request.session["nonuser"], completed=False)
            #     if Cart.objects.filter(user=request.user, completed=False).exists():
            #         cart.user = None
            #         cart.save()
                    
            #     else:
            #         cart.user = request.user
            #         cart.save()
            
            # except:
            #     pass
            
            return redirect('index')

        else:
            print("Invalid credentials provided")
    context = {}
    return render(request, "login.html", context)



def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("index")


