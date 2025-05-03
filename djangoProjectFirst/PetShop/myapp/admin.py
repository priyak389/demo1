from django.contrib import admin
from .models import petFood,PetFoodDetails,pet,Customer,PetProduct,ProdCategory,cart,customerDetails,Orders

# Register your models here.
class petFoodAdmin(admin.ModelAdmin):
    list_display=['petFoodId','petFoodName','foodPrice','foodDesc','price','pet']

admin.site.register(petFood,petFoodAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display=['uid','pid','qty']
admin.site.register(cart,cartAdmin)

 
class customeradmin(admin.ModelAdmin):
    list_display=['user','custname','custEmail','custAddress','custcontact','pincode']
admin.site.register(customerDetails,customeradmin)

class petFoodDetailsadmin(admin.ModelAdmin):
    list_display=['petFood','company','expiryDate']
admin.site.register(PetFoodDetails,petFoodDetailsadmin)
 
class petadmin(admin.ModelAdmin):
    list_display=['petName','petCat']
admin.site.register(pet,petadmin)


class custadmin(admin.ModelAdmin):
    list_display=['custId','custName','custEmail','custContact']
admin.site.register(Customer,custadmin)



class prodadmin(admin.ModelAdmin):
    list_display=['prodName','prodDesc','prodPrice','prodImage','prodRating','cat','is_deleted','delete_details']
admin.site.register(PetProduct,prodadmin)

class prodcatadmin(admin.ModelAdmin):
    list_display=['categoryName','catDesc']
admin.site.register(ProdCategory,prodcatadmin)

 
class orderadmin(admin.ModelAdmin):
    list_display=['customer','pet','quantity','order_date','status','total_price']
admin.site.register(Orders,orderadmin)
 


 

 
