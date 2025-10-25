from django.db import models
from datetime import datetime, timedelta
import random
from django.utils import timezone


from django.db import models

class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)  # Matches MySQL's int NO PRI
    airline_name = models.CharField(max_length=20, null=True, blank=True)
    origin = models.CharField(max_length=20, null=True, blank=True)
    destination = models.CharField(max_length=20, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    total_seats = models.IntegerField(null=True, blank=True)
    available_seats = models.IntegerField(null=True, blank=True)
    base_price = models.FloatField(null=True, blank=True)
    airline_tier = models.CharField(max_length=20, default="Standard", null=True, blank=True)
    demand_level = models.FloatField(default=1.0, null=True, blank=True)

    class Meta:
        db_table = 'flights'  # Ensures Django uses your existing MySQL table

    def __str__(self):
        return f"{self.flight_id} - {self.airline_name} ({self.origin} → {self.destination})"



class Passenger(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default="Unknown")
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],default='Other')
    email = models.EmailField(unique=True,null=True, blank=True)
    phone = models.BigIntegerField(unique=True)

    class Meta:
        db_table = 'passengers'
    def __str__(self):
        return self.name

from datetime import date

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE,db_column='passenger_id')
    booking_date = models.DateTimeField(auto_now_add=True)

    travel_date = models.DateField(default=date.today)
    seat_preference = models.CharField(max_length=10,default='Window')  # Add this
    total_fare = models.FloatField()  # Add this
    STATUS_CHOICES = [('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')  # ✅ Add this

    seat_no = models.CharField(max_length=5, null=True, blank=True)
    pnr = models.CharField(max_length=15, unique=True, null=True, blank=True)

    class Meta:
        db_table = 'bookings'

    def __str__(self):
        return f"{self.pnr} - {self.passenger.name}"
