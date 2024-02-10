from django import forms
from core.models import Review
from django.core.validators import MaxLengthValidator


class ReviewForm(forms.ModelForm):
    user = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"user"}))
    occupation = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Occupation","id":"occupation"}))
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Short title for the review","id":"title"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Email", "class": "form-control ","id":"email"}))
    review = forms.CharField(widget=forms.Textarea(attrs={"id":"message","class":"message-area","placeholder": "Leave us a review...."}), validators=[MaxLengthValidator(130, message='Please enter at most 130 characters')])
    
    class Meta:
        model = Review
        fields = ['user','occupation','email','title','review']