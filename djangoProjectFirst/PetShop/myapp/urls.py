 
from django.urls import path
from .import views
urlpatterns = [
  
    path('',views.show,name="home"),
    path('contactus',views.contactus),
    

    path('crudOperation',views.crudoperation),
    
    path('myView',views.SimpleView.as_view()),
    path('showdetails',views.showdetails),

    path('delete/<int:id>/',views.deletecust),

    path('edit/<int:id>/',views.edit),
    path('register/',views.register,name='register'),
    path('loginuser/',views.loginuser,name='loginuser'),
    path('logout/',views.signout,name='signout'),
    path('cat/<int:id>/',views.category,name='cat'),
    path('viewproduct/<int:id>/',views.viewproduct,name='viewproduct'),

    path('addcart/<int:id>/',views.addtocart,name='addtocart'),
    
    path('addproduct',views.addproduct,name='addproduct'),

    path('deleteproductcrud/<int:id>/',views.deleteproductcrud,name="deleteproductcrud"),
    
    path('viewcart/',views.viewcart,name="viewcart"),
    
    path('updateqty/<qv>/<id>/',views.updateqty),

    path('searchdata',views.searchdata,name="searchdata"),

    path('remove/<int:id>',views.remove,name='remove'),
    path('customerdetails/',views.customerdetails,name="customerdetails"),
    path('checkout',views.checkout,name='checkout'),
    path('paymentsuccess',views.paymentsuccess,name='paymentsuccess'),
    path('paymentfailed',views.paymentfailed,name='paymentfailed'),

    path('forgot-password/',views.forgot_password, name='forgot_password'),

    path('reset_password',views.reset_password,name='reset_password'),

    path('sent_otp',views.send_otp,name='sent_otp'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    
    path('orders/',views.orders,name='orders'),
    path('drf_crud/',views.crudapi.as_view()),

]
