from django.urls import path
from . import views

urlpatterns = [
    path('officeBookings/', views.office_booking_list_create, name='office-booking-list-create'),
    path('schoolBookings/', views.school_booking_list_create, name='school-booking-list-create'),
]