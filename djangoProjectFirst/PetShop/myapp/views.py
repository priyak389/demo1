from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from datetime import datetime
from .models import Customer,ProdCategory,PetProduct,cart,customerDetails,Orders
from .forms import petproductform,RegisterForm,userAuthentication,PetProductForm,customerDetailsform
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
import uuid

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse


# Create your views here.
def show(request):
    # return render(request,'index.html',{'name':'Nikhil','Msg':'How are you!'})
    # return render(request,'index.html',{'x':0,'y':10})
    # context={}
    # context["prodList"]=["P101","Mobile",60000,"Mobile device"]
    # date_details=datetime.now()
    # return render(request,'index.html',{'prodId':"p101","ProdName":"Samsung mobile","Price":60000,"datedetails":date_details})
    category=ProdCategory.objects.all() #retrive all data from model ProdCategory
    active_products = PetProduct.objects.active()
    print("Active products are",active_products)
    products=PetProduct.objects.filter(is_deleted=False)
    
    context={'category':category,'products':products}
    return render(request,'index.html',context)

def viewproduct(request,id):
    products=PetProduct.objects.filter(id=id)
    return render(request,'viewproduct.html',{'products':products})


# view to show add to cart functionality
@login_required(login_url='loginuser')
def addtocart(request,id):
    # Basic implementation
    # prod=PetProduct.objects.filter(id=id)
    # print(prod)
    # addtocartprod=cart.objects.create(pid=prod[0])
    # addtocartprod.save()
    # return HttpResponse("Product added to cart")
    userid=request.user.id
    user_details=User.objects.filter(id=userid)
    products=PetProduct.objects.filter(id=id)
    print(products)
    q1=Q(pid=products[0])
    q2=Q(uid=user_details[0])
    prod=cart.objects.filter(q1 & q2)
    n=len(prod)
    context={}
    context['products']=products
    if n==1:
        context['msg']="Already in cart!!! Please check"
        return render(request,'viewproduct.html',context)
    else:
        addtocartprod=cart.objects.create(pid=products[0],uid=user_details[0])
        addtocartprod.save()
        context['success']="Successfully Added to cart!!!"
        return render(request,'viewproduct.html',context)
    
#to show products from cart
def viewcart(request):
    userid=request.user.id 
    print(userid)
    products=cart.objects.filter(uid=userid)
    print(products)
    total=0
    for i in products:
        total=total+i.pid.prodPrice*i.qty
    
    
    del_charge=200
    total=del_charge+total

    return render(request,'viewcart.html',{'products':products,'total':total})






def updateqty(request,qv,id):
     c=cart.objects.filter(id=id)
     if qv=='1':
         t=c[0].qty+1
         c.update(qty=t)
     else:
         if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)

     return redirect('/viewcart')


import random
from django.core.mail import send_mail

def send_otp(request):
    if request.method == "POST":
        user_email = request.user.email  
        otp = random.randint(100000, 999999)  

     
        request.session['payment_otp'] = otp

       
        subject = "Your OTP for Payment Verification"
        message = f"Dear {request.user.username},\n\nYour OTP for payment verification is: {otp}\n\nPlease enter this OTP to proceed with your payment.\n\nBest Regards,\nYour Pet Store Team"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,   
            [user_email], 
            fail_silently=False
        )

        return redirect('verify_otp')   

    return render(request, 'sent_otp.html')
 


from django.contrib import messages

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')   
        stored_otp = request.session.get('reset_otp')   
        otp_purpose = request.session.get('otp_purpose', '')  

        if stored_otp and entered_otp == str(stored_otp):  
             
            if otp_purpose == "login":  
                return redirect('reset_password')   
            # elif otp_purpose == "payment":
            #     return redirect('checkout')  
            # else:
            #     return redirect('checkout')   

        else:
            messages.error(request, "Invalid OTP! Please try again.")
    
    return render(request, 'verify_otp.html') 

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
     
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()  
            otp = random.randint(100000, 999999)  
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            request.session['otp_purpose'] = "login"

            subject = "Your Password Reset OTP"
            message = f"Dear {user.username},\n\nYour OTP for password reset is: {otp}\n\nPlease enter this OTP to reset your password.\n\nBest Regards,\nYour Support Team"

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('verify_otp')  # Redirect to OTP verification page

        else:
            messages.error(request, "Email not found! Please enter a registered email.")
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')

def reset_password(request):
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        email = request.session.get('reset_email')

        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                # Clear session data
                del request.session['reset_otp']
                del request.session['reset_email']

                messages.success(request, "Password reset successful! You can now login.")
                return redirect('loginuser')

            except User.DoesNotExist:
                messages.error(request, "Something went wrong. Try again.")
                return redirect('forgot_password')
        else:
            messages.error(request, "Passwords do not match! Try again.")
            return render(request, 'reset_password.html')

    return render(request, 'reset_password.html')
 
def customerdetails(request):
    if request.method=="POST":
        fm=customerDetailsform(request.POST)
        if fm.is_valid():
            customer=fm.save(commit=False)
            customer.user=request.user
            customer.save()
            return redirect('checkout')
        
        

    else:
        fm=customerDetailsform()
        return render(request,'customerdetails.html',{'form':fm})

def checkout(request):
    userid=request.user.id 
    print(userid)
    products=cart.objects.filter(uid=userid)
    print(products)
    
    total=0
    for i in products:
        total=total+i.pid.prodPrice*i.qty
    del_charge=200
    total=del_charge+total

    customer=customerDetails.objects.filter(user=userid)
    
    
  #================= Paypal Code =====================
   
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
        'amount': total,    #: The amount of money to be charged for the transaction. 
        'item_name': 'Petproduct',       # Describes the item being purchased.
        'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
        'return_url': f"http://{host}{reverse('paymentsuccess')}",     #The URL where the customer will be redirected after a successful payment. 
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

  #================= Paypal Code  End =====================

   

    return render(request,'checkout.html',{'products':products,'total':total,'customer':customer,
                                           'paypal_payment':paypal_payment})

def paymentsuccess(request):
    userid=request.user.id 
    print(userid)
    user_email = request.user.email 
    print(user_email)
    products=cart.objects.filter(uid=userid)
    print(products)
    total=0
    for i in products:
        total=total+i.pid.prodPrice*i.qty
        del_charge=200
        total=del_charge+total

        order=Orders.objects.create(customer=i.uid,pet=i.pid,quantity=i.qty,total_price=total)
        order.save()
        i.delete()
    orders=Orders.objects.filter(customer=request.user.id)
    subject = "Payment Successful - Order Confirmation"
    message = f"Dear {request.user.username},\n\nYour payment was successful!\nTotal Amount: ₹{total}\nThank you for shopping with us.\n\nBest Regards,\nYour Pet Store Team"
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender email (configured in settings.py)
        [user_email],  # Recipient email
        fail_silently=False
    )

    return render(request,'paymentsucess.html',{'orders':orders})

def orders(request):
    orders=Orders.objects.filter(customer=request.user.id)

    return render(request,'orders.html',{'orders':orders})

def paymentfailed(request):
    return render(request,'paymentfailed.html')



def searchdata(request):
    if request.method=="POST":
        searchData=request.POST['search']
        print(searchData)
        result=PetProduct.objects.filter(prodName__contains=searchData)
        print(result)
        
        return render(request,'search.html',{'result':result})
    else:
        return render(request,'search.html')

def remove(request,id):
    product=cart.objects.filter(id=id)
    print(product)
    product.delete()


    return redirect('viewcart')

def addproduct(request):
    if request.method=="POST":
         productform=PetProductForm(request.POST,request.FILES)
         if productform.is_valid():
            productform.save()
            return redirect('home')
         else:
            return redirect('addproduct')
    
    else:
        productform=PetProductForm()
        return render(request,'addproductcrud.html',{'form':productform})



def crudoperation(request):
    if request.method=="POST":
        print("Request is",request.method)
        custId=request.POST['custid']  #1
        custName=request.POST['custname']#PRIYA
        custemail=request.POST['custemail']#techpy111@gmail.com
        custContact=request.POST['custcontact']#9999999999
        cust=Customer.objects.create(custId=custId,custName=custName,custEmail=custemail,custContact=custContact)
        cust.save()
        return redirect('/showdetails')
        
    else:
        print("Request is",request.method)
        return render(request,'crud_operation.html')

def showdetails(request):
    custdetails=Customer.objects.all()
    
    return render(request,'dashboard.html',{'custdetails':custdetails})

def deletecust(request,id):
    custdetails=Customer.objects.filter(id=id)
    custdetails.delete()
    return redirect('/showdetails')


def deleteproductcrud(request,id):
    product=PetProduct.objects.get(id=id,is_deleted=False)
    product.is_deleted=True
    product.delete_details=timezone.now()
    product.save()
    return redirect('home')






def edit(request,id):
    if request.method=="POST":
        print("Request is",request.method)
        custId=request.POST['custid']  
        custName=request.POST['custname']
        custemail=request.POST['custemail']
        custContact=request.POST['custcontact']
        
        m=Customer.objects.filter(id=id)

        m.update(custId=custId,custName=custName,custEmail=custemail,custContact=custContact)
        
        return redirect('/showdetails')
    else:
        custdetails=Customer.objects.get(id=id)
        return render(request,'edit.html',{'custdetails':custdetails})




def contactus(request):
    return HttpResponse("Contact us")


def register(request):
    # pd=petproductform()

    if request.method=="POST":
        registerForm=RegisterForm(request.POST)
        print(registerForm)
        if registerForm.is_valid():
            registerForm.save()
            return redirect('home')
        else:
            return redirect('register')

    else:

        registerForm=RegisterForm()
        return render(request,'register.html',{'registerForm':registerForm})

from django.contrib.auth import authenticate,login,logout
import datetime
def loginuser(request):
    if request.method=="POST":
        uname=request.POST['username']
        upass=request.POST['password']
        print(uname)
        print(upass)
        user=authenticate(request,username=uname,password=upass)
        print(user)
        if user is not None:
            login(request,user)
            request.session['last_activity'] = str(datetime.datetime.now())
            request.session.set_expiry(10) 
            response=redirect('home')
            request.session['username']=uname
            response.set_cookie('Username',uname)
            response.set_cookie('time',datetime.datetime.now())
            return response         
      
        

        else:
            return redirect('loginuser')
    else:
        userform=userAuthentication()
        return render(request,'loginuser.html',{'userform':userform})
    
    
def signout(request):
    logout(request)
    return redirect('home')

def category(request,id):
    print(id)
    category=ProdCategory.objects.all()
    products=PetProduct.objects.filter(cat=id)
    return render(request,'index.html',{'category':category,'products':products})


class SimpleView(View):
    def get(self,request):
        return HttpResponse("hello")
    def post(self,request):
        return HttpResponse("hii")
    

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import customerSerializer

class crudapi(APIView):
    def get(self,request):
        id=request.data.get('id',None)
        if id:
            try:
                customer=customerDetails.objects.get(id=id)
                customerdata=customerSerializer(customer)
                print(customerdata)
                return Response(customerdata.data,status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Data is not available'},status=status.HTTP_404_NOT_FOUND)
        
        else:
            customer=customerDetails.objects.all()
            print(customer)
            customerdata=customerSerializer(customer,many=True)

            print(customerdata)
            return Response(customerdata.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        customerdetails=request.data 
        print(customerdetails)
        customerdata=customerSerializer(data=customerdetails)
        print(customerdata)
        if customerdata.is_valid():
            customerdata.save()
            return Response({'Msg':'Data is successfully inserted'},status=status.HTTP_200_OK)
        return Response({'msg':'Data is not available'},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request):
        new_data=request.data 
        id=new_data.get('id',None)
        print(id)
        if id:
            try:
                customer_data=customerDetails.objects.get(id=id)
                print(customer_data)
                customer_data=customerSerializer(customer_data,new_data,partial=True)
                if customer_data.is_valid():
                    customer_data.save()
                    return Response({'Msg':'Data is successfully updated'},status=status.HTTP_200_OK)
            except:
                return Response({'Msg':'data is not available'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request):
        id=request.data.get('id',None)
        if id:
            try:
                customer=customerDetails.objects.get(id=id)
                customer.delete()
                 
                return Response({'msg':'Data is successfully deleted'},status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Data is not available'},status=status.HTTP_404_NOT_FOUND)
        
           
        return Response({'Msg':'Please provide id'},status=status.HTTP_200_OK)
     