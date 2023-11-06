from django.urls import path

from . import views

app_name="donor"
urlpatterns=[
    path("login",views.login,name='login')
]