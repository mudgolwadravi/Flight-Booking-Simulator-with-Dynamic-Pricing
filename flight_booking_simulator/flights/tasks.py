
from .models import Flight
import random

def update_demand():
    flights = Flight.objects.all()
    for f in flights:
        f.demand_level = round(random.uniform(0.8, 1.6), 2)
        f.seats_available = max(5, f.seats_available - random.randint(0, 5))
        f.save()
