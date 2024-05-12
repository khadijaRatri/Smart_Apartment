from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Apartment(models.Model):
    apartment_id = models.IntegerField(primary_key=True)
    apartment_no = models.CharField(max_length=100)
    apartment_size = models.CharField(max_length=100)
    status_choice = (
        ('Occupied', 'Occupied'),
        ('Vacant', 'Vacant')
    )
    apartment_status = models.CharField(max_length=100, choices=status_choice, blank=True, null=True)

    def __str__(self):
        return self.apartment_no


class Owner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_id = models.IntegerField(primary_key=True)
    owner_name = models.CharField(max_length=100)
    owner_email = models.EmailField()
    owner_NID = models.CharField(max_length=20)
    owner_contactNo = models.CharField(max_length=15)
    owned_apartments = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    owner_image = models.ImageField(upload_to='static/images', blank=True, null=True)

    def __str__(self):
        return f'{self.owner_name} : {self.owned_apartments.apartment_no}'


class Resident(models.Model):
    resident_id = models.IntegerField(primary_key=True)
    resident_name = models.CharField(max_length=100)
    resident_email = models.EmailField()
    resident_NID = models.CharField(max_length=20)
    resident_contactNo = models.CharField(max_length=15)
    residing_apartments = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    resident_image = models.ImageField(upload_to='static/images', blank=True, null=True)

    def __str__(self):
        return f'Resident name : {self.resident_name}-{self.residing_apartments.apartment_no}'


class Guest(models.Model):
    guest_id = models.IntegerField(primary_key=True)
    guest_name = models.CharField(max_length=100)
    guest_contactNo = models.CharField(max_length=15)
    checkInDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    visited_apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.guest_name}-{self.visited_apartment.apartment_no}'


class Amenity(models.Model):
    amenity_id = models.IntegerField(primary_key=True)
    amenity_name = models.CharField(max_length=100)
    amenity_description = models.TextField(blank=True, null=True)
    amenity_status = models.CharField(max_length=50)
    amenity_image = models.ImageField(upload_to='static/images', blank=True, null=True, default='images/default.jpg')

    def __str__(self):
        return self.amenity_name


class Service(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=100)
    service_description = models.TextField(blank=True, null=True)
    service_status = models.CharField(max_length=50)
    service_image = models.ImageField(upload_to='static/images', blank=True, null=True, default='images/default.jpg')

    def get_absolute_url(self):
        return f"/service/{self.service_id}"

    def __str__(self):
        return self.service_name


class AmenityRequest(models.Model):
    amenityReq_id = models.IntegerField(primary_key=True)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status_choice = (
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
        ('Not Available', 'Not Available'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Closed', 'Closed'),
    )
    status = models.CharField(max_length=100, choices=status_choice, blank=True, null=True)
    request_time = models.DateTimeField(auto_now_add=True, auto_now=False)


class ServiceRequest(models.Model):
    serviceReq_id = models.IntegerField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status_choice = (
        ('Available', 'Available'),
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('In-progress', 'In-progress')
    )
    status = models.CharField(max_length=100, choices=status_choice, blank=True, null=True)
    request_time = models.DateTimeField(auto_now_add=True, auto_now=False)


class Complaint(models.Model):
    complaint_id = models.IntegerField(primary_key=True)
    complaint_content = models.CharField(max_length=100, blank=True, null=True)
    complaint_description = models.TextField(blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, null=True)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Complain {self.complaint_id}: {self.complaint_content}'


class Statement(models.Model):
    statement_id = models.IntegerField(primary_key=True)
    statement_choice = (
        ('Previous-Month-Statement', 'Previous-Month-Statement'),
        ('Monthly-Statement', 'Monthly-Statement'),
        ('Yearly-Statement', 'Yearly-Statement')
    )
    status = models.CharField(max_length=100, choices=statement_choice, blank=True, null=True)
    statement_details = models.TextField(blank=True, null=True)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)


class BillPayment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Amount: {self.payment_amount}, Time: {self.payment_time}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='static/images', default='images/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'


class UserAccount(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

