from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import TextInput


class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    class Meta:
        model=models.CustomUser
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].required=True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create related Patient instance
            models.Patient.objects.create(
                user=user
                
                # Add other fields as needed
            )
        return user

class PatientForm(forms.ModelForm):
    
    class Meta:
        model=models.Patient
        fields=['age','bloodgroup','disease','address','doctorname','mobile','profile_pic']

#class PatientLoginForm(forms.ModelForm):
    
  #  class Meta:
    #    model=models.Patient
  #      fields=['username','password']
   #     widgets = {
   #     'password': forms.PasswordInput()
   #     }
        

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(render_value=True)
        self.fields['password2'].widget = forms.PasswordInput(render_value=True)

class PatientLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Fields: {self.fields}")
