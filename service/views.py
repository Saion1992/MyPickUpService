from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .models import OfficeBooking, SelectedDay, SchoolBooking
from .serializers import OfficeBookingSerializer, SchoolBookingSerializer
from django_ratelimit.decorators import ratelimit

@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def office_booking_list_create(request):
    data = request.data
    mobile = data.get('mobile')
    existing_booking = OfficeBooking.objects.filter(mobile=mobile).first()

    if existing_booking:
        # Phone number matches, update existing entry
        updated_fields = False
        updated_name = data.get('name')
        new_selected_days = data.get('selected_days', [])

        if existing_booking.name != updated_name:
            existing_booking.name = updated_name
            updated_fields = True

        if existing_booking.pickup_location != data.get('pickup_location'):
            existing_booking.pickup_location = data.get('pickup_location')
            updated_fields = True

        if existing_booking.drop_location != data.get('drop_location'):
            existing_booking.drop_location = data.get('drop_location')
            updated_fields = True

        if existing_booking.pickup_time != data.get('pickup_time'):
            existing_booking.pickup_time = data.get('pickup_time')
            updated_fields = True

        if existing_booking.return_time != data.get('return_time', None):
            existing_booking.return_time = data.get('return_time', None)
            updated_fields = True

        if existing_booking.want_return != data.get('want_return'):
            existing_booking.want_return = data.get('want_return')
            updated_fields = True

        existing_selected_days = set(existing_booking.selected_days.values_list('day', flat=True))
        if set(existing_selected_days) != set(new_selected_days):
            existing_booking.selected_days.clear()
            for selected_day in new_selected_days:
                day, created = SelectedDay.objects.get_or_create(day=selected_day)
                existing_booking.selected_days.add(day)
            updated_fields = True

        if updated_fields:
            existing_booking.save()
            serializer = OfficeBookingSerializer(existing_booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # Phone number doesn't match, create a new entry
        selected_days_data = data.get('selected_days', [])
        booking = OfficeBooking.objects.create(
            name=data['name'],
            mobile=data['mobile'],
            pickup_location=data.get('pickup_location'),
            drop_location=data.get('drop_location'),
            gender=data.get('gender'),
            pickup_time=data.get('pickup_time'),
            return_time=data.get('return_time', None),
            want_return=data.get('want_return')
        )

        for selected_day in selected_days_data:
            day, created = SelectedDay.objects.get_or_create(day=selected_day)
            booking.selected_days.add(day)

        serializer = OfficeBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def school_booking_list_create(request):
    data = request.data
    mobile = data.get('mobile')
    existing_booking = SchoolBooking.objects.filter(mobile=mobile).first()

    if existing_booking:
        updated_fields = False
        updated_name = data.get('name')

        if existing_booking.name != updated_name:
            existing_booking.name = updated_name
            updated_fields = True

        if existing_booking.pickup_location != data['pickup_location']:
            existing_booking.pickup_location = data['pickup_location']
            updated_fields = True

        if existing_booking.drop_location != data['drop_location']:
            existing_booking.drop_location = data['drop_location']
            updated_fields = True

        if existing_booking.pickup_time != data.get('pickup_time'):
            existing_booking.pickup_time = data.get('pickup_time')
            updated_fields = True

        if existing_booking.return_time != data.get('return_time'):
            existing_booking.return_time = data.get('return_time')
            updated_fields = True

        if existing_booking.age != data.get('age'):
            existing_booking.age = data.get('age')
            updated_fields = True

        if existing_booking.date != data.get('date'):
            existing_booking.date = data.get('date')
            updated_fields = True

        if updated_fields:
            existing_booking.save()
            serializer = SchoolBookingSerializer(existing_booking)
            return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        booking, created = SchoolBooking.objects.get_or_create(
            name=data['name'],
            age=data['age'],
            mobile=data['mobile'],
            pickup_location=data['pickup_location'],
            drop_location=data['drop_location'],
            gender=data['gender'],
            pickup_time=data.get('pickup_time'),
            return_time=data.get('return_time'),
            date=data['date']
        )

        if created:
            serializer = SchoolBookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Booking already exists'}, status=status.HTTP_409_CONFLICT)

    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)