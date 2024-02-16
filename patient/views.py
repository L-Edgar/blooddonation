from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from django.contrib.auth import login, authenticate
from blood import models as bmodels
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

def loginView(request):
    messages.success(request,'')
    print(f"Request method: {request.method}")
    if request.method=='POST':
        loginform=forms.PatientUserForm(request.POST)

        if loginform.is_valid():
            username=loginform.cleaned_data['username']
            password=loginform.cleaned_data['password']
            existing_user=User.objects.filter(username=username).first()
            if existing_user:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request,user)
                    return redirect('patient_dashboard_view')
                else:
                    messages.info(request,'Invalid Credentials')
                    return redirect('loginView')
            else:
                messages.info(request, 'User does not exist')
                return redirect('loginView')
        else:
            print(f"Form errors: {loginform.errors}")
            
    else:
        loginform = forms.PatientUserForm()  # An unbound form
        print("unsuccessful")
        
    return render(request,'patient/patientlogin.html',{'loginform':loginform})



def logout(request):
    auth.logout(request)
    return redirect("blood/logout.html")

def patient_signup_view(request):
    #userForm=forms.PatientUserForm()
    #patientForm=forms.PatientForm()
    #mydict={'userForm':userForm,'patientForm':patientForm}
    userForm=forms.CustomUserCreationForm()
    
    
    if request.method=='POST':
        userForm=forms.CustomUserCreationForm(request.POST)
        #userForm=forms.PatientUserForm(request.POST)
        #patientForm=forms.PatientForm(request.POST,request.FILES)
        
            
        if userForm.is_valid():
            password1=userForm.cleaned_data['password1']
            password2=userForm.cleaned_data['password2']
            username=userForm.cleaned_data['username']
            
            if password1==password2:
                 if forms.CustomUserCreationForm.Meta.model.objects.filter(username=username).exists():
                    messages.error(request, 'Passwords do not match.')
                    
                    return render(request, 'patient/patientsignup.html', {'userForm': userForm})
                    
                 else:
                    userForm.save()
                    #user.set_password(user.password)
                    
                    
                #patient=patientForm.save(commit=False)
                #patient.user=user
                #patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
                #patient.save()
                #my_patient_group = Group.objects.get_or_create(name='PATIENT')
                #my_patient_group[0].user_set.add(user)
                    return redirect('/patient/patientlogin')
        else:
            print(userForm.errors)
    else:
        userForm=forms.CustomUserCreationForm()
        print('Error 3')
    return render(request,'patient/patientsignup.html',{'userForm': userForm})

@login_required(login_url='patientlogin')
def patient_dashboard_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html',context=dict)

@login_required(login_url='patientlogin')
def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient= models.Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})

@login_required(login_url='patientlogin')
def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})


@login_required(login_url='patientlogin')
def patient_profile(request):
    return render(request,'patient/patient_profile.html')