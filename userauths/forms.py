from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from userauths.models import Contact, Booking, Service
from userauths.countries import COUNTRIES
from django.core.validators import MinLengthValidator
class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"first_name"}))
    country = forms.ChoiceField(choices=COUNTRIES, widget=forms.Select(attrs={"class": "form-control ","id":"homeland"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "emma@gmail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"first_name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"last_name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Email", "class": "form-control ","id":"email"}))
    country = forms.ChoiceField(choices=COUNTRIES, widget=forms.Select(attrs={"class": "form-control-country ","id":"homeland"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"id":"message","placeholder": "Leave us a message...."}), validators=[MinLengthValidator(15, message='Please enter at least 15 characters')])
    
    class Meta:
        model = Contact
        fields = ['first_name','last_name','email','country','message']

class BookingForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"first_name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"last_name"}))
    business_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"last_name"}))
    company_type = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Company Type","class": "form-control","id":"company_type"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Email", "class": "form-control ","id":"email"}))
    country = forms.ChoiceField(choices=COUNTRIES, widget=forms.Select(attrs={"class": "form-control ","id":"homeland"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"id":"message","placeholder": "Leave us a message...."}), validators=[MinLengthValidator(10, message='Please enter at least 15 characters')])
    company_needs = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={}),
    )
    class Meta:
        model = Booking
        fields = ['first_name','last_name','email','country','message',"company_needs","company_type", "business_name"]