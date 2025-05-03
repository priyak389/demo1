from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import PetProduct,customerDetails

class petproductform(forms.Form):
    petproductNmae=forms.CharField()
    petproductprice=forms.DecimalField()
    petproductdesc=forms.CharField()

class RegisterForm(UserCreationForm):
    password1=forms.CharField(label="Enter Password:",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

        labels={
            'username':'Enter Username',
            'first_name':'Enter first Name',
            'last_name':'Enter last name',
            'email':'Enter Email'
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already exist. Please use a different email.")
            return email

class userAuthentication(AuthenticationForm):
    username=forms.CharField(label='Enter username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="Enter Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model=User
        fields=['username','password']


class PetProductForm(forms.ModelForm):
    class Meta:
        model=PetProduct
        fields=['prodName','prodDesc','prodPrice','prodImage','prodRating','cat']

    def clean_prodName(self):
        prodName = self.cleaned_data.get('prodName')
        if not prodName.isalpha():
            raise forms.ValidationError("Product name must contain only alphabets.")
        return prodName


class customerDetailsform(forms.ModelForm):
    class Meta:
        model=customerDetails
        fields=['custname','custEmail','custAddress','custcontact','pincode']
 
 
