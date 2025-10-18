
from .models import Flight
import random

def update_demand():
    flights = Flight.objects.all()
    for f in flights:
        f.demand_level = round(random.uniform(0.8, 1.6), 2)
        f.seats_available = max(5, f.seats_available - random.randint(0, 5))
        f.save()

from celery import shared_task
from .views import calculate_dynamic_price
import random

@shared_task
def update_flight_market():
    flights = Flight.objects.all()
    for flight in flights:
        change = random.randint(-3, 3)
        flight.available_seats = max(0, min(flight.total_seats, flight.available_seats + change))
        flight.demand_level = round(random.uniform(0.8, 1.5), 2)
        flight.save()
