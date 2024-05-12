from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.http import HttpResponse

# Create your views here.


@unauthenticated_user
def signUp(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='resident')
                user.groups.add(group)

                messages.success(request, 'Account was created for' + username )
                return redirect('login')

        context = {'form': form}
        return render(request, template_name='system/signUp.html', context=context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name

                if group == 'manager':
                    return redirect('manager_dashboard')
                elif group == 'owner':
                    return redirect('owner_dashboard')
                elif group == 'resident':
                    return redirect('resident_dashboard')
                elif group == 'gatekeeper':
                    return redirect('gatekeeper_dashboard')

            else:
                messages.info(request, message='Username or Password is incorrect.')
                return render(request, template_name='system/login.html')

    return render(request, template_name='system/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, template_name='home.html')


@login_required(login_url='login')
@allowed_users(['manager'])
def manager_dashboard(request):
    # Your manager dashboard logic here
    return render(request, 'system/manager_dashboard.html')


@login_required(login_url='login')
@allowed_users(['owner'])
def owner_dashboard(request):
    # Your owner dashboard logic here
    return render(request, 'system/owner_dashboard.html')


@login_required(login_url='login')
@allowed_users(['resident'])
def resident_dashboard(request):
    # Your resident dashboard logic here
    return render(request, 'system/resident_dashboard.html')


@login_required(login_url='login')
@allowed_users(['gatekeeper'])
def gatekeeper_dashboard(request):
    # Your gatekeeper dashboard logic here
    return render(request, 'system/gatekeeper_dashboard.html')


@login_required(login_url='login')
@allowed_users(['owner', 'manager'])
def apartment(request):
    apartments = Apartment.objects.all()
    context = {
        'apartments': apartments,
    }
    return render(request, template_name='system/apartment.html', context=context)


@login_required(login_url='login')
@allowed_users(['owner', 'manager'])
def update_apartment(request, apartment_id):
    apartments = Apartment.objects.get(pk = apartment_id)
    form = ApartmentForm(instance=apartments)

    if request.method =="POST":
        form = ApartmentForm(request.POST, instance=apartments)
        if form.is_valid():
            form.save()
            return redirect('apartment')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_apartment.html', context=context)


@login_required(login_url='login')
@allowed_users(['manager'])
def upload_apartment(request):
    form = ApartmentForm()
    if request.method =='POST':
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('apartment')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_apartment.html', context=context)


@login_required(login_url='login')
@allowed_users(['gatekeeper', 'resident', 'manager', 'owner'])
def guestList(request):
    guests = Guest.objects.all()
    context = {
        'guests': guests,
    }
    return render(request, template_name='system/guestList.html', context=context)


@login_required(login_url='login')
@allowed_users(['gatekeeper'])
def update_guest(request, guest_id):
    guests = Guest.objects.get(pk = guest_id)
    form = GuestForm(instance=guests)

    if request.method =="POST":
        form = GuestForm(request.POST, instance=guests)
        if form.is_valid():
            form.save()
            return redirect('guestList')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_guest.html', context=context)


@login_required(login_url='login')
@allowed_users(['gatekeeper'])
def upload_guest(request):
    form = GuestForm()
    if request.method =='POST':
        form = GuestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guestList')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_guest.html', context=context)


@login_required(login_url='login')
def resident(request):
    residents = Resident.objects.all()
    context = {
        'residents': residents,
    }
    return render(request, template_name='system/resident.html', context=context)


@login_required(login_url='login')
def service(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, template_name='system/service.html', context=context)


def request_service(request,service_id):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.service = Service.objects.get(id=service_id)
            # Create a new service request object
            service_request.save()
            return redirect('service_request_list')# Redirect back to the service list page
    else:
        form = ServiceRequestForm()
    return render(request, 'system/service_request.html', {'form': form})


def service_request_list(request):
    requests = ServiceRequest.objects.all()
    return render(request, 'request_list.html', {'requests': requests})


def service_details(request, service_id):
    services = Service.objects.get(service_id = service_id)
    context = {
        'services': services,
    }
    return render(request, template_name='system/service_details.html', context=context)


@allowed_users(['manager'])
def upload_service(request):
    form = ServiceForm()
    if request.method =='POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_service.html', context=context)


@allowed_users(['manager'])
def update_service(request, service_id):
    services = Service.objects.get(pk = service_id)
    form = ServiceForm(instance=services)

    if request.method =="POST":
        form = ServiceForm(request.POST, request.FILES, instance=services)
        if form.is_valid():
            form.save()
            return redirect('service')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_service.html', context=context)


@allowed_users(['manager'])
def delete_service(request, service_id):
    services = Service.objects.get(pk = service_id)
    if request.method == 'POST':
        services.delete()
        return redirect('service')
    return render(request, template_name='system/delete_service.html')


def amenity(request):
    amenities = Amenity.objects.all()
    context = {
        'amenities': amenities,
    }
    return render(request, template_name='system/amenity.html', context=context)


def amenity_details(request, amenity_id):
    amenities = Amenity.objects.get(pk = amenity_id)
    context = {
        'amenities': amenities,
    }
    return render(request, template_name='system/amenity_details.html', context=context)


@allowed_users(['manager'])
def upload_amenity(request):
    form = AmenityForm()
    if request.method =='POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('amenity')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_amenity.html', context=context)


@allowed_users(['manager'])
def update_amenity(request, amenity_id):
    amenities = Amenity.objects.get(pk = amenity_id)
    form = AmenityForm(instance=amenities)
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES, instance=amenities)
        if form.is_valid():
            form.save()
            return redirect('amenity')

    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_amenity.html', context=context)


@allowed_users(['manager'])
def delete_amenity(request, amenity_id):
    amenities = Amenity.objects.get(pk = amenity_id)
    if request.method == 'POST':
        amenities.delete()
        return redirect('amenity')
    return render(request, template_name='system/delete_amenity.html')


@login_required(login_url='login')
@allowed_users(['manager', 'resident', 'owner'])
def complain(request):
    complains = Complaint.objects.all()
    context = {
        'complains': complains,
    }
    return render(request, template_name='system/complain.html', context=context)


@login_required(login_url='login')
@allowed_users(['resident', 'owner'])
def upload_complain(request):
    form = ComplaintForm()
    if request.method =='POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('complain')
    context = {
        'form' : form
    }
    return render(request, template_name='system/upload_complain.html', context=context)


def bill_payment_form(request):
    if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = BillPaymentForm()
    context = {'form': form}
    return render(request, template_name='bill_payment_form.html', context=context)


@login_required(login_url='login')
@allowed_users(['resident', 'owner'])
def payments_list(request):
    payments = BillPayment.objects.all()
    context = {'payments': payments}
    return render(request, template_name='system/payments_list.html', context=context)


def success_page(request):
    return render(request, template_name='success_page.html')

