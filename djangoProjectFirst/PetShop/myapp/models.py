from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
 
'''
model-
      Model is class defined in models.py, file in application directory
      when settings.py file is executed django tries to connect with db maintain in the db settings.
      Default database given by django is sqlite3.

      model-defining/creating tables in db.
      model is representative of table in database.
      


     
      
      any modelclass(petFood) defined must be inherited from Model class which is inside models 
      module 

      A model is the single, definitive source of information about your data. It contains the 
      essential fields and behaviors of the data you’re storing. Generally, each model maps to a 
      single database table.

   
    
    The basics:

    Each model is a Python class that subclasses django.db.models.Model.

    Each attribute of the model represents a database field.


    datatypes in models:
    Thee are inbuilt function in models module that are used to assign data type 
    to data members which are going to be column in the table

    type of data        function in models module
    varchar(20)              models.CharField(max_length=100)
    int                      models.IntegerField()
    float                    models.FloatField()
    email                    models.EmailField()
    decimal                  models.DecimalField(max_digits=7,decimal_places=2)
    date                     models.DateField()
    price                    models.PositiveIntegerField()

    connect mysql to django
    pip install mysqlclient
    python manage.py showmigrations  (check migrations)
    python manage.py makemigrations  (create migrations)
    python maange.py migrate       

    built in field validations:
    1.null: if True django will store empty value as null in db default is False
    2.Blank: if True the field is allowed to be blank default is False
    3.default: default value for the field
               address :mumbai
    4.help_text-:Extra help text to be displayed in form widgets
    5.primary_key:if True this field is pk for model
    6.error_messages:override the default msg that the field will raise
    7.unique:unique value provide

    ORM:
    Django includes a default object relational mapping(ORM) that can be used to interact with data 
    from various relational db such as sqlite3,postgreSQL and mysql

    Django allows us to add delete modify and query objects using ORM
    It provides a layer between relational db and object oriented Programming language
    without having to write sql queries


   Relationship in Django model:
   1.One to One relationship:
   One record of perticular model is related to exactly one record of another model

   data integrity:
   Refers to accuracy of data in db
   we need to define the behaviour of a record in one model when the corresponding record 
   in another model is deleted

   1.on_delete=models.CASCADE:
   default setting
   it ensures that all the related records in the linked model are also deleted when record into 
   one model is deleted
   2.on_delete=models.PROTECT:
   it ensures that the deletion of the record having relationship with other record is blocked

   3.on_delete=models.SET_NULL:
     when a record is deleted it assigns NULL to the relational fieed if null=True is set

   4.on_delete=models.SET_DEFAULT:
      it provides default values to relational field when a record is deleted & default value is
      provide

2.Many to one relationship:
   pet(M)-petfood(1)

3.many to many relationship:
pet(M)-petfood(M)



'''


class pet(models.Model):
    petName=models.CharField(max_length=100)
    petCat=models.CharField(max_length=100)
    def __str__(self):
        return self.petName
    

class petvaccine(models.Model):
    vaccineName=models.CharField(max_length=100)
    pet=models.ManyToManyField(pet)
    
class petFood(models.Model):
    petFoodId=models.IntegerField()
    petFoodName=models.CharField(max_length=100)
    foodPrice=models.DecimalField(max_digits=7,decimal_places=2)
    foodDesc=models.TextField(null=True,blank=True)
    price=models.PositiveIntegerField()
    pet=models.ForeignKey(pet,on_delete=models.PROTECT,null=True,blank=True)

    def __str__(self):
        return self.petFoodName


class PetFoodDetails(models.Model):
    petFood=models.OneToOneField(petFood,on_delete=models.CASCADE)
    company=models.CharField(max_length=100)
    expiryDate=models.DateField()


# custom validation
def validation_Email(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of gmail only")

class Customer(models.Model):
    custId = models.IntegerField()
    custName = models.CharField(max_length=100)
    custEmail = models.CharField(max_length=200, validators=[validation_Email])
    custContact=models.BigIntegerField(null=True,blank=True)

    def __str__(self):
        return self.custName



class ProdCategory(models.Model):
    categoryName=models.CharField(max_length=100)
    catDesc=models.TextField()
    def __str__(self):
        return self.categoryName

class PetProductManager(models.Manager):
    def active(self):
        return self.filter(is_deleted=False)
    
class PetProduct(models.Model):
    prodName=models.CharField(max_length=100)
    prodDesc=models.TextField()
    prodPrice=models.DecimalField(max_digits=7,decimal_places=2)
    prodImage=models.ImageField(upload_to='images/')
    prodRating=models.DecimalField(max_digits=2,decimal_places=1)
    cat=models.ForeignKey(ProdCategory,on_delete=models.CASCADE,null=True,blank=True)
    is_deleted=models.BooleanField(default=False)
    delete_details=models.DateTimeField(null=True,blank=True)
    objects = PetProductManager()
    def __str__(self):
        return self.prodName
    




class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid',null=True,blank=True)
    pid=models.ForeignKey(PetProduct,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
  


class Orders(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(PetProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return f"Order #{self.id} - {self.status}"



class customerDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    custname=models.CharField(max_length=100)
    custEmail=models.EmailField()
    custAddress=models.TextField()
    custcontact=models.BigIntegerField()
    pincode=models.IntegerField()

    def __str__(self):
        return self.custname
    




















