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
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    email = models.EmailField(unique=True,null=True, blank=True)
    phone = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)  # 👈 This tells Django to use booking_id
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seat_no = models.CharField(max_length=5)
    total_fare = models.FloatField()
    STATUS_CHOICES = [('Confirmed','Confirmed'),('Cancelled','Cancelled')]
    seat_no = models.CharField(max_length=5, null=True, blank=True)
    pnr = models.CharField(max_length=15, unique=True, null=True, blank=True)


    class Meta:
        db_table = 'bookings'  # 👈 This maps to your existing MySQL table

    def __str__(self):
        return f"{self.pnr} - {self.passenger.name}"

