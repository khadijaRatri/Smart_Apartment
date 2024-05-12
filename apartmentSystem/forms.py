from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class ApartmentForm(ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class AmenityForm(ModelForm):
    class Meta:
        model = Amenity
        fields = '__all__'


class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'


class BillPaymentForm(ModelForm):
    class Meta:
        model = BillPayment
        fields = ['payment_amount', 'resident']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ServiceRequestForm(ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service']

