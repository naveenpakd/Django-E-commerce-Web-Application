from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from . forms import CustomerProfileForm
import razorpay
from django.conf import settings
from django.utils.decorators import method_decorator



# Create your views here.
def contact(request):
    return render(request,"contact.html")

def index(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'index.html',locals())


# @login_required(login_url='login')
def collections(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    category=Category.objects.filter(status=0)
    return render(request,'collections.html',locals())

def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,"invalid username or password")
            return redirect('login')
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,"username already exists")
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.info(request,"email already exists")
            return redirect('register')
        
        else:
            user=User.objects.create_user(username=username , email=email, password=password)
            user.save();
        return redirect('/')
    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def collectionsview(request,slug):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    if (Category.objects.filter(slug=slug, status=0)):
        product=Product.objects.filter(category__slug=slug)
    else:
        messages.error(request,"no ")
        return redirect('collections')
    return render(request,'product.html',locals())



def productview(request, cate_slug, prod_slug):
    # context = {}

    if Category.objects.filter(slug=cate_slug, status=0).exists():
        if Product.objects.filter(slug=prod_slug, status=0).exists():
            product = Product.objects.get(slug=prod_slug, status=0)
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        return redirect('collections')
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = Cart.objects.filter(user=request.user, product=product).exists()
        context = {
            'product': product,
            'item_already_in_cart': item_already_in_cart
        }
        # if item_already_in_cart:
        #     # messages.info(request, "This item is already in your cart")
            

    return render(request, 'productview.html',locals())



    

@login_required(login_url='login')
def cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'cart.html',locals())

@login_required(login_url='login')
def add_to_cart(request):
    user = request.user
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    quantity = 1  # Set the quantity of the product

    Cart(user=user, product=product, product_qty=quantity).save()
    return redirect("/cart")


@login_required(login_url='login')
def show_cart(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    # print(card_product)
    if cart_product:
        for p in cart_product:
            tempamount = (p.product_qty * p.product.selling_price)
            amount += tempamount
            totalamount = amount 
        return render(request, 'addtocart.html',locals())
    else:
        return render(request, 'emptycard.html',locals())
    

@method_decorator(login_required, name='dispatch')   
class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0.0
        for p in cart_items:
            value = p.product_qty * p.product.selling_price
            famount += value
        totalamount = famount
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)

        order_id = payment_response['id']
        order_status = payment_response['status']
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, "checkout.html", locals())
    

@login_required(login_url='login')
def payment_done(request):
    user = request.user
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    print(order_id,payment_id,cust_id)
    customer = Customer.objects.get(id=cust_id)
    print(id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.product_qty,payment=payment).save()
        c.delete()
    return redirect("orders")



    
       

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'order_placed': op, 'totalitem': totalitem})

@login_required(login_url='login')
def plus_card(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.product_qty += 1
    c.save()

    amount = 0.0
    # shipping_amount = 70.0
    card_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in card_product:
        tempamount = (p.product_qty * p.product.selling_price)
        amount += tempamount

    data = {
        'quantity': c.product_qty,
        'amount': amount,
        'totalamount': amount 
    }
    return JsonResponse(data)

@login_required(login_url='login')
def minus_card(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.product_qty -= 1
    c.save()

    amount = 0.0
    
    card_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in card_product:
        tempamount = (p.product_qty * p.product.selling_price)
        amount += tempamount

    data = {
        'quantity': c.product_qty,
        'amount': amount,
        'totalamount': amount 
    }
    return JsonResponse(data)

@login_required(login_url='login')
def remove_card(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    

    amount = 0.0
    
    card_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    for p in card_product:
        tempamount = (p.product_qty * p.product.selling_price)
        amount += tempamount
        

    data = {
        'amount': amount,
        'totalamount': amount 
    }
    
    return JsonResponse(data)
  

@login_required(login_url='login')
def check_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')

    if product_id:
        try:
            cart_item = Cart.objects.get(user=user, product_id=product_id)
            item_in_cart = True
        except Cart.DoesNotExist:
            item_in_cart = False
    else:
        cart_items_count = Cart.objects.filter(user=user).count()
        item_in_cart = cart_items_count > 0

    data = {
        'item_in_cart': item_in_cart
    }

    return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'profile.html', locals())
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
        user = request.user
        name = form.cleaned_data['name']
        localty = form.cleaned_data['localty']
        city = form.cleaned_data['city']
        mobile = form.cleaned_data['mobile']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']
        reg = Customer(user=user,name=name,localty=localty,city=city,mobile=mobile,state=state,zipcode=zipcode)
        reg.save()
    
        
        messages.success(request,"Congragulation Profile Save Successfully")
        return redirect("address")
    else:
        messages.warning(request,'invalid input data')
    return render(request,"profile.html",locals())
  

@login_required(login_url='login')  
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request,"address.html",locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"updateAddress.html",locals())
    def post (self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.localty = form.cleaned_data['localty']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
        return render(request, "updateAddress.html",locals())

@login_required(login_url='login')    
def UpdateDelete(request, pk):
    add = Customer.objects.get(pk=pk)
    add.delete()
    messages.success(request, "Profile deleted successfully")
    return redirect("address")

    






    
