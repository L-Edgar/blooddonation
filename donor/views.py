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
from blood import models as bmodels
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib.auth import logout as auth_logout
from ip2geotools.databases.noncommercial import DbIpCity
import requests
import logging
import json
from functools import wraps


logger = logging.getLogger(__name__)

def donorlogin(request):
    #messages.success(request,'')
    print(f"Request method: {request.method}")
    if request.method=='POST':
        
        loginform=forms.DonorUserForm(request.POST)
       # if loginform.is_valid():
            
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.role=='donor':
            login(request,user)
            return redirect('donor:donor-dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect("donor:donorlogin")
        #else:
           # print(f"Form errors: {loginform.errors}")
            
    else:
        loginform = forms.DonorUserForm()  # An unbound form
        print("unsuccessful")
        
    return render(request,'donor/donorlogin.html',{'loginform':loginform})

def donor_signup_view(request):
    #userForm=forms.DonorUserForm()
    
    userForm=forms.CustomUserCreationForm()
    #donorForm=forms.DonorForm()
    mydict={'userForm':userForm}
    if request.method=='POST':
        #userForm=forms.DonorUserForm(request.POST)
        #donorForm=forms.DonorForm(request.POST,request.FILES)
        userForm=forms.CustomUserCreationForm(request.POST)
        if userForm.is_valid():
            #user=userForm.save()
            #user.set_password(user.password)
            #user.save()
            #donor=donorForm.save(commit=False)
            #donor.user=user
            #donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            #donor.save()
            #my_donor_group = Group.objects.get_or_create(name='DONOR')
            #my_donor_group[0].user_set.add(user)
            password1=userForm.cleaned_data['password1']
            password2=userForm.cleaned_data['password2']
            username=userForm.cleaned_data['username']
            print(userForm.cleaned_data)
            if password1==password2:
                 if forms.CustomUserCreationForm.Meta.model.objects.filter(username=username).exists():
                    messages.error(request, 'Passwords do not match.')
                    
                    return render(request, 'patient/patientsignup.html', {'userForm': userForm})
                    
                 else:
                    user = userForm.save(commit=False)
                    user.role = 'donor'
                    user.set_password(password1)
                    user.save()
                    
                    return redirect('donor:donorlogin')
            else:
                print(userForm.errors)
        else:
            messages.error(request,userForm.errors)
            #print(userForm.errors)
            #userForm=forms.CustomUserCreationForm()
            
    else:
        print(userForm.errors)
        
        
    return render(request,'donor/donorsignup.html',context=mydict)

def check_donor_registration(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        donor=models.Donor.objects.filter(user_id=request.user.id).first()
        if not donor:
            return redirect('donor:complete-reg')
        if not (donor.bloodgroup or donor.mobile or donor.address or donor.profile_pic):
            return redirect('donor:complete-reg')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url='donorlogin')
def complete_registration(request):
    donor = models.Donor.objects.filter(user_id=request.user.id).first()
    
    print("First User:", request.user)

    if request.method=='POST':
        user_form=forms.DonorForm(request.POST,request.FILES,instance=donor)
        if user_form.is_valid():
            print("Third User:", request.user)
            user_form.instance.user = request.user
            user_form.save()
            print("Successful")
            
            redirect_url = request.GET.get('next', 'donor:donor-dashboard')
            return redirect(redirect_url)
            

        else:
            print("Error: ", user_form.errors)
            print("Second User:", request.user)

    else:
        
        user_form = forms.DonorForm(instance=donor)
        
    return render(request,"donor/donor_registration.html",{"user_form":user_form})

@login_required(login_url='donorlogin')
def donor_dashboard_view(request):
    donor= models.Donor.objects.filter(user_id=request.user.id).first()
    if not donor:
        default_counts = {
                'requestpending': 0,
                'requestapproved': 0,
                'requestmade': 0,
                'requestrejected': 0,
            }
        return render(request, 'donor/donor_dashboard.html', context=default_counts)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


@login_required(login_url='donorlogin')
@check_donor_registration
def donate_blood_view(request):
    print("User ID:", request.user.id)
    
    
    
    donation_form=forms.DonationForm()
    if request.method=='POST':
        donation_form=forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
            
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor=donor
            blood_donate.save()
            return HttpResponseRedirect('donation-history') 
        print("Form is not valid",donation_form.errors)  
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})


@login_required(login_url='donorlogin')
@check_donor_registration
def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})
    


@login_required(login_url='donorlogin')
@check_donor_registration
def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.filter(user_id=request.user.id).first()
            blood_request.request_by_donor=donor
            blood_request.save()
            return HttpResponseRedirect('request-history')  
    return render(request,'donor/makerequest.html',{'request_form':request_form})


@login_required(login_url='donorlogin')
@check_donor_registration
def request_history_view(request):
    donor= models.Donor.objects.filter(user_id=request.user.id).first()
            
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})
    

@login_required(login_url='donorlogin')
def donor_profile(request):
    donor= models.Donor.objects.filter(user_id=request.user.id).first()
    
    return render(request,'donor/donor_profile.html',{'donor':donor})

def logout_view(request):
    auth_logout(request)
    return render(request,"blood/logout.html")



