from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Product
from django_email_verification import send_email
from .forms import UserRegistrationForm,CustomerProfileForm
from django.contrib import messages
from .models import Customer,Cart,OrderPlaced
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid 
import razorpay
client = razorpay.Client(auth=("rzp_test_K38R9q1TXDmpTK", "6scgGY3RhpqXTL9cF1K0uoNx"))

def home(request):
    lowers = Product.objects.filter(catagory = 'l')
    tshirts = Product.objects.filter(catagory = 'ts')
    tracksuits = Product.objects.filter(catagory = 't')
    return render(request, 'app/home.html',{'lowers' :lowers, 'tshirts' :tshirts, 'tracksuits' :tracksuits})

def product_detail(request,pid):
    product = Product.objects.get(id=pid)
    isInCart = Cart.objects.filter(user= request.user).filter(product=product)
   
   
    if isInCart.count() == 0:
      button = {
      'id' : 1,
      'text' : 'Add To Cart',
      'classname' : 'btn btn-primary'
      }
      return render(request, 'app/productdetail.html',{'product':product,'button':button})
    else :
      button = {
      'id' : 2,
      'text' : 'Go To Cart',
      'classname' : 'btn btn-warning'
      }
      return render(request, 'app/productdetail.html',{'product':product,'button':button})  
def delete_from_cart(request,itemid):
  Cart.objects.filter(id = itemid).delete()
  messages.success(request,'Cart Item Deleted Successfully')
  return redirect('/cart/')

@login_required
def add_to_cart(request,pid = None):
  if pid != None :
    product = Product.objects.get(id=pid)
    cartitem = Cart(user = request.user, product = product)
    cartitem.save()
    messages.success(request, 'Product added successfully to the Cart')
    
    return redirect('/product-detail/' + str(pid)); 
  else :
    cartitems = Cart.objects.filter(user = request.user)
    amount = 0.0

    for item in cartitems :
      amount += item.quantity*item.product.discounted_price
    print (amount)  
    return render(request, 'app/addtocart.html',{'cartitems': cartitems,'amount' : amount})

def pluscart(request):
  id = request.GET.get('id')
  
  product = Cart.objects.filter(id=id).first()
  product.quantity +=1
  product.save()
  cartitems = Cart.objects.filter(user = request.user)
  amount = 0.0

  for item in cartitems :
      amount += item.quantity*item.product.discounted_price

  data = {
    'quantity' : product.quantity,
    'amount' : amount,
  }    
  print (data)
  return JsonResponse(data)    

def minuscart(request):
  id = request.GET.get('id')
  product = Cart.objects.filter(id=id).first()
  product.quantity -=1
  product.save()
  cartitems = Cart.objects.filter(user = request.user)
  amount = 0.0

  for item in cartitems :
      amount += item.quantity*item.product.discounted_price
  data = {
    'quantity' : product.quantity,
    'amount' : amount,
  }    
  return JsonResponse(data)    

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def profile(request):
  if( request.method == 'GET'):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html', {'form': form})
  if(request.method == 'POST'):
    form = CustomerProfileForm(request.POST)

    if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            pincode=form.cleaned_data['pincode']
            reg= Customer(user=user,name=name,locality=locality,city=city,state=state,pincode=pincode)
            reg.save()
            messages.success(request,'Your Adress has been registered, Move to Adress section to edit or view, Happy Shopping !')
            return redirect('/profile')

def checklogin(request):
  addresses = Customer.objects.filter(user=request.user)

  if addresses.count() == 0 :
    return redirect('/profile')
  else:
    return redirect('/')  
def address(request):
  addresses = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{'addresses' : addresses})

@login_required
def orders(request):
  orders = OrderPlaced.objects.filter(user=request.user)

  return render(request, 'app/orders.html',{'orders' : orders})


def tshirts(request,data= None):
  if (data == None) :
    tshirts = Product.objects.filter(catagory = 'ts')  
  else:
    tshirts = Product.objects.filter(catagory ='ts').filter(brand = data)
  return render(request, 'app/tshirt.html',{'tshirts':tshirts})



def customerregistration(request):
    if(request.method == 'GET'):
        form = UserRegistrationForm()
        
        return render(request, 'app/customerregistration.html' ,{'form' : form})

    if (request.method == 'POST'):
        form = UserRegistrationForm(request.POST)

        print (form)
        if form.is_valid():
            # user = User(username = form.cleaned_data['username'],email = form.cleaned_data['email'],password = form.cleaned_data['password1'])
            user = form.save(commit=False)
            
            
            user.is_active = False
            user.save()
            
            
            
            send_email(user)
            messages.success(request,'Account activiating mail have been sent to You, Kindely activate your account and then Proceed to login')
            # form.save()
        
        
            return redirect('/accounts/login')
        else :
          return render(request, 'app/customerregistration.html' ,{'form' : form})
@login_required
def checkout(request,data=None):
  un_id = uuid.uuid4().hex[:6].upper()
  if data == None:
    addresses = Customer.objects.filter(user=request.user)
    cartitems = Cart.objects.filter(user = request.user)
    
    
    
    amount = 0.0
  # razor pay
    for item in cartitems :
      amount += item.quantity*item.product.discounted_price
    order_amount = amount*100
    order_currency = 'INR'
    # order_receipt = 'order_rcptid_11'
    # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
    # receipt=order_receipt, notes=notes
    payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1 ))
    payment_order_id=payment_order['id']
    
   
    return render(request, 'app/checkout.html',{'addresses': addresses,'cartitem':cartitems,'totalamount':amount,'un_id' : un_id,'order_id':payment_order_id,'api_key':"rzp_test_K38R9q1TXDmpTK"})
  else:
    addresses = Customer.objects.filter(user=request.user)
    product = Product.objects.filter(id = data).first()
    cartitems = []
    cartitem = Cart(user = request.user,product = product)
    cartitem.save()
    cartitems.append(cartitem)
    amount = 0.0
  # razor pay
    for item in cartitems :
      amount += item.quantity*item.product.discounted_price
    order_amount = amount*100
    order_currency = 'INR'
    # order_receipt = 'order_rcptid_11'
    # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
    # receipt=order_receipt, notes=notes
    payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1 ))
    payment_order_id=payment_order['id']
    
   
    return render(request, 'app/checkout.html',{'addresses': addresses,'cartitem':cartitems,'totalamount':amount,'un_id' : un_id,'order_id':payment_order_id,'api_key':"rzp_test_K38R9q1TXDmpTK"})

@csrf_exempt
def checkoutdone(request):
  cart = Cart.objects.filter(user = request.user)
  addid = request.GET.get('custid')
 
  customer = Customer.objects.filter(id = addid).first()
  messages.success(request,'Your payment was successful , Here is your order tranking tab')

  for product in cart:
    OrderPlaced(user = request.user,customer = customer,product = product.product,quantity = product.quantity).save()
    product.delete()
  return redirect('orders')  