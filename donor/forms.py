from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()



#class DonorUserForm(UserCreationForm):
 #   class Meta:
  #      model=User
   ##    widgets = {
        #'password': forms.PasswordInput()
     #   'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
      #  'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
       # }

    #def __init__(self,*args,**kwargs):
     #   super(DonorUserForm,self).__init__(*args,**kwargs)
      #  #self.fields['password'].required=False
       # for field_name,field in self.fields.items():
        #   field.widget.attrs['class']='form-control'

class DonorForm(forms.ModelForm):
    class Meta:
        model=models.Donor
        fields=['bloodgroup','address','mobile','profile_pic','date_of_birth']

        def __init__(self, *args, **kwargs):
            # Call the base class method
            super(DonorForm, self).__init__(*args, **kwargs)
            # Make the address field read-only
           
            
   # user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput())
   # def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user', None)
    #    super(DonorForm, self).__init__(*args, **kwargs)

    #    if user:
     #       self.fields['user'].initial = user
     #       self.fields['user'].widget.attrs['disabled'] = True 

    #def save(self, commit=True):
    #    instance = super(DonorForm, self).save(commit=False)
    #    instance.user = self.cleaned_data['user']
    #    if commit:
     #       instance.save()
     #   return instance

class DonationForm(forms.ModelForm):
    class Meta:
        model=models.BloodDonate
        fields=['age','bloodgroup','disease','unit']


class CustomUserCreationForm(UserCreationForm):
    role = forms.CharField(max_length=20, initial='donor',required=False) 
    class Meta:
        model =CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'role']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(render_value=True)
        self.fields['password2'].widget = forms.PasswordInput(render_value=True)
   

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Fields: {self.fields}")