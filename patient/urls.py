from django.urls import path

from . import views

app_name="patient"
urlpatterns=[
    path("login/",views.login,name='login')
]