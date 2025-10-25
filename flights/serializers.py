from rest_framework import serializers
from .models import Flight, Passenger, Booking


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'




class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingRequestSerializer(serializers.Serializer):
    flight_id = serializers.IntegerField()
    passenger_id = serializers.IntegerField()
    seat_no = serializers.CharField(required=False, allow_blank=True)
    travel_date = serializers.DateField()
    seat_preference = serializers.CharField(max_length=10)



