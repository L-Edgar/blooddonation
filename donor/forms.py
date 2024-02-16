from django import forms
from django.contrib.auth.models import User
from . import models


class DonorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].required=False

class DonorForm(forms.ModelForm):
    class Meta:
        model=models.Donor
        fields=['bloodgroup','address','mobile','profile_pic']

class DonationForm(forms.ModelForm):
    class Meta:
        model=models.BloodDonate
        fields=['age','bloodgroup','disease','unit']
