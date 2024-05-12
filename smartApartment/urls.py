"""
URL configuration for smartApartment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings
from apartmentSystem import views as a_view
from apartmentSystem import views as b_view
from apartmentSystem import views as s_view
from apartmentSystem import views as am_view
from apartmentSystem import views as d_view
from apartmentSystem import views as ap_view
from apartmentSystem import views as g_view
from apartmentSystem import views as c_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', a_view.home, name='home'),
    path('signUp/', a_view.signUp, name='signUp'),
    path('login/', a_view.loginPage, name='login'),
    path('logout/', a_view.logoutUser, name='logout'),
    path('owner_dashboard/', d_view.owner_dashboard, name='owner_dashboard'),
    path('resident_dashboard/', d_view.resident_dashboard, name='resident_dashboard'),
    path('manager_dashboard/', d_view.manager_dashboard, name='manager_dashboard'),
    path('gatekeeper_dashboard/', d_view.gatekeeper_dashboard, name='gatekeeper_dashboard'),
    path('service/<str:service_id>/', s_view.service_details, name='service_details'),
    path('upload_service/', s_view.upload_service, name='upload_service'),
    path('update_service/<str:service_id>', s_view.update_service, name='update_service'),
    path('delete_service/<str:service_id>', s_view.delete_service, name='delete_service'),
    path('service/<str:service_id>/', s_view.request_service, name='request_service'),
    path('request_service/', s_view.request_service, name='request_service'),
    path('apartment/', ap_view.apartment, name='apartment'),
    path('upload_apartment/', ap_view.upload_apartment, name='upload_apartment'),
    path('update_apartment/<str:apartment_id>', ap_view.update_apartment, name='update_apartment'),
    path('resident/', a_view.resident, name='resident'),
    path('service/', s_view.service, name='service'),
    path('amenity/', am_view.amenity, name='amenity'),
    path('amenity/<str:amenity_id>/', am_view.amenity_details, name='amenity_details'),
    path('upload_amenity/', am_view.upload_amenity, name='upload_amenity'),
    path('update_amenity/<str:amenity_id>', am_view.update_amenity, name='update_amenity'),
    path('delete_amenity/<str:amenity_id>', am_view.delete_amenity, name='delete_amenity'),
    path('bill-payment/', b_view.bill_payment_form, name='bill_payment_form'),
    path('payments-list/', b_view.payments_list, name='payments_list'),
    path('success/', b_view.success_page, name='success_page'),
    path('guestList/', g_view.guestList, name='guestList'),
    path('upload_guest/', g_view.upload_guest, name='upload_guest'),
    path('update_guest/<str:guest_id>', g_view.update_guest, name='update_guest'),
    path('complain/', c_view.complain, name='complain'),
    path('upload_complain/', c_view.upload_complain, name='upload_complain'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
