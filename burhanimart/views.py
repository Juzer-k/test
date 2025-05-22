from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from burhanimart.models import ContactUs, CustomerAddress, OrderPlaced, Product, SliderBanner, Cart
from .forms import Contact, RegistrationForm, Address
from django.contrib.auth.decorators import login_required
# import stripe
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your BurhaniMart Account Created Successfully!!!!')
            return render(request,'signup.html',{'form':form})
    else:
        form = RegistrationForm()
        return render(request, 'signup.html',{'form':form})
    return render (request,'signup.html',{'form':form})

def slider(request, id):
    slider = SliderBanner.objects.get(id = id)
    print('hello')
    print(slider)
    return render (request, 'home.html',{'slider':slider})

def home(request):
    cloth_category_product = Product.objects.filter(Q(product_category = 'cloth') & Q(product_sub_category = 'rida') | Q(product_sub_category = 'kurta_izar') | Q(product_sub_category = 'night_dress'))
    jewellery_category_product = Product.objects.filter(Q(product_category = 'emitation_jewellery'))
    return render(request, 'home.html',{'cloth_category_product':cloth_category_product , 'jewellery_category_product':jewellery_category_product})

def productdetail(request, id):
    product_detail = Product.objects.get(id =id)
    product_already_in_cart = False
    if request.user.is_authenticated:
        product_already_in_cart = Cart.objects.filter(Q(product = product_detail.id) & Q(user=request.user)).exists()  # type: ignore
    return render(request, 'product_detail.html',{'product_detail':product_detail, 'product_already_in_cart':product_already_in_cart})

def cloth_category(request):
    cloth_category = Product.objects.filter(product_category = 'cloth')
    return render(request,'cloth_category.html', {'cloth_category':cloth_category})

def all_category(request):
    category = Product.objects.filter(Q(product_category = 'cloth') | Q(product_category = 'emitation_jewellery') | Q(product_category = 'topi') | Q(product_category = 'rida'))
    return render(request, 'all_category.html',{'category':category})

# Cart functions
@login_required(login_url='login')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product_already_in_cart = Cart.objects.filter(Q(product = product_id) & Q(user=request.user)).exists()
    if product_already_in_cart == False:
        product = Product.objects.get(id = product_id)
        Cart(user=user,product = product).save()
    return redirect('/view-cart-product')

@login_required(login_url='login')  # type: ignore
def view_cart_product(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        shipping_amount = 50
        totalamount=0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.product_discounted_price)
                amount += tempamount
                totalamount = amount+shipping_amount
                return render(request, 'view_cart_product.html', {'cart':cart, 'amount':amount, 'totalamount':totalamount})
        else:
            return render(request, 'empty_cart.html')
    else:
        return render(request, 'empty_cart.html')

@login_required(login_url='login')    
def minus_cart_product(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cart.quantity-=1
        cart.save()
        amount = 0
        shipping_amount= 50
        cart_product = [prod for prod in Cart.objects.all() if prod.user == request.user]
        for prod in cart_product:
            temporary_amount = (prod.quantity * prod.product.product_discounted_price)
            amount += temporary_amount
        data = {
			'quantity':cart.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
        return JsonResponse(data)
    else:
        return HttpResponse("")

@login_required(login_url='login')    
def add_cart_product(request):
    if request.method == 'GET':
        prod_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0
        shipping_amount= 50
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.product_discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
            amount += tempamount
			# print("After", amount)
		# print("Total", amount)

        data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
        return JsonResponse(data)
    else:
        return HttpResponse("")


@login_required(login_url='login')    
def remove_cart_item(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cart.delete()
        amount = 0
        shipping_amount= 0
        cart_product = [prod for prod in Cart.objects.all() if prod.user == request.user]
        for prod in cart_product:
            temporary_amount = (prod.quantity * prod.product.product_discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
            amount += temporary_amount
			# print("After", amount)
		# print("Total", amount)
        data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
        return JsonResponse(data)
    else:
        return HttpResponse("")

# function for add new address     Address CRUD Operation
@login_required(login_url='login')
def add_new_address(request):
    if request.method == 'POST':
        form = Address(request.POST)
        if form.is_valid():
            current_user = request.user
            customer_name  = form.cleaned_data['customer_name']
            mobile_number = form.cleaned_data['mobile_number']
            area_locality = form.cleaned_data['area_locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            user_address = CustomerAddress(user=current_user, customer_name=customer_name, mobile_number=mobile_number ,area_locality=area_locality, city=city, state=state, zip_code=zip_code)
            user_address.save()
            messages.success(request, 'Address Added Successfully')
            return render(request,'add_new_address.html',{'form':form})
    else:
        form = Address()
        return render(request,'add_new_address.html',{'form':form}) 
    return render(request,'add_new_address.html',{'form':form}) 
# function for render saves address  
@login_required(login_url='login')    
def save_address(request):
    save_address = CustomerAddress.objects.filter(user = request.user)
    return render(request, 'save_address.html',{'save_address':save_address})
# function for update address 
@login_required(login_url='login')         
def update_address(request, id):
    if request.method == 'POST':
        current_address = CustomerAddress.objects.get(pk = id)
        change_address = Address(request.POST , instance = current_address)
        if change_address.is_valid():
            change_address.save()
    else:
        current_address = CustomerAddress.objects.get(pk = id)
        change_address = Address(instance = current_address)
        return render(request, 'update_address.html',{'form': change_address})
    return HttpResponseRedirect('/save-address')
# function for delete address   
@login_required(login_url='login')      # type: ignore
def delete_save_address(request , id):
    if request.method == 'POST':
        address = CustomerAddress.objects.get(pk = id)
        address.delete()
        messages.error(request,'Address Deleted Successfully')
        return HttpResponseRedirect('/save-address')
    
@login_required(login_url='login')    
def checkout(request):
    user = request.user
    current_address = CustomerAddress.objects.filter(user=user)
    cart_product = Cart.objects.filter(user=request.user)
    amount = 0
    shipping_amount = 50
    totalamount=0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    print(cart_product)
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.product_discounted_price)
            amount += tempamount
            totalamount = amount+shipping_amount
    return render(request, 'checkout.html', {'current_address':current_address, 'cart_product':cart_product, 'totalamount':totalamount, 'amount':amount})

@login_required(login_url='login')    
def order_placed_successfully(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    customeraddressid = request.GET.get('customeraddressid')
    current_address = CustomerAddress.objects.get(id =customeraddressid)
    amount = 0
    amount1 = 0
    total_amount = 0
    shipping_amount= 50
    product_amount = 0
    cart_item = [prod for prod in Cart.objects.all() if prod.user == request.user] #list comprehension
    if cart_item:
        for prod in cart_item:
            product_amount = prod.product.product_discounted_price
            amount += product_amount

            tempamount1 = (prod.quantity * prod.product.product_discounted_price)
            amount1 += tempamount1
            total_amount = amount1 + shipping_amount 
    for cart_product in cart:
        OrderPlaced(user = user , address = current_address , product = cart_product.product , quantity = cart_product.quantity, amount = product_amount, total_amount = total_amount).save()
        print('order save')
        cart_product.delete()
        print('cart product deleted')
    return render(request, 'order_placed_successfully.html')

@login_required(login_url='login')    
def order_view(request):
    user = request.user
    order_placed = OrderPlaced.objects.filter(user = user).order_by('-id')
    return render(request, 'order_view.html',{'order_placed':order_placed})

@login_required(login_url='login')    
def order_detail(request, id):
    order_detail = OrderPlaced.objects.get(id =id)
    return render(request, 'order_detail.html',{'order_detail':order_detail})

def search_product(request):
    search_product_query = request.GET.get('query')
    product_search_match = Product.objects.filter(Q(product_name__icontains = search_product_query) | Q(product_category__icontains = search_product_query))
    return render(request,'search_product.html',{'product_search_match':product_search_match,'search_product_query':search_product_query})

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['customer_name']
            email = form.cleaned_data['customer_email']
            mobile_number = form.cleaned_data['mobile_number']
            query = form.cleaned_data['query']
            query_sent = ContactUs(user=user, customer_name = name , customer_email = email, mobile_number = mobile_number,query = query)
            query_sent.save()
            messages.success(request,'We have Recived your Query . ')
            return render(request, 'contact_us.html',{'form':form})
    else:
        form = Contact()
        return render(request , 'contact_us.html',{'form':form})

    return render(request, 'contact_us.html',{'form':form})

@login_required(login_url='login')    
def account_detail(request):
    return render(request , 'account_detail.html')