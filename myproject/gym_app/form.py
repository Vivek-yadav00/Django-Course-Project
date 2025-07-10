from django import forms
from .models import Member,Contact

class MemberForm(forms.ModelForm):
    class Meta:
        model=Member
        fields=["name","age"]

        
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=["email","phone"]
        label={'email':'Email Address','phone':'Phone Number'}