from multiprocessing import AuthenticationError
from django import forms
from .models import *
from .Templates import *
from ckeditor.fields import RichTextField

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'discount', 'quantity', 'category', 'brand','Product_details']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    role = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=ROLE_CHOICES, 
        initial='buyer'
    )

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'email', 'phone_number']