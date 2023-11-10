from django.urls import path
from . import views

urlpatterns = [
    path('office-booking/', views.office_booking_list_create, name='office-booking-list-create'),
    path('school-booking/', views.school_booking_list_create, name='school-booking-list-create'),
    # Other URL patterns for your app
]