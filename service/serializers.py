from rest_framework import serializers
from .models import OfficeBooking, SelectedDay, SchoolBooking

class SelectedDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedDay
        fields = '__all__'

class OfficeBookingSerializer(serializers.ModelSerializer):
    selected_days = SelectedDaySerializer(many=True)

    class Meta:
        model = OfficeBooking
        fields = '__all__'

class SchoolBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolBooking
        fields = '__all__'