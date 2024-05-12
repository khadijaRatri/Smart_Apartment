from django.contrib import admin
from .models import Apartment, Owner, Resident, Guest, Amenity, Service, AmenityRequest, ServiceRequest, Complaint, Statement, BillPayment, UserAccount

# Register your models here.

admin.site.register([Apartment, Owner, Resident, Guest, Amenity, Service, AmenityRequest, ServiceRequest, Complaint, Statement, BillPayment, UserAccount])