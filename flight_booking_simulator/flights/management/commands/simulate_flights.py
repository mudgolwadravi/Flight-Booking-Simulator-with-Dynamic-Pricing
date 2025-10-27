import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from flights.models import Flight


class Command(BaseCommand):
    help = "Generate at least 250 upcoming flights with realistic timings and prices"

    def handle(self, *args, **kwargs):
        # Clear old data
        Flight.objects.all().delete()

        # Common Indian city routes
        cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Jaipur", "Ahmedabad", "Goa"]
        airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air"]

        flights_created = 0

        for _ in range(250):  # Create 250 flights minimum
            origin, destination = random.sample(cities, 2)

            # Ensure only future flights (from tomorrow onwards)
            dep_time = datetime.now() + timedelta(days=random.randint(1, 10), hours=random.randint(0, 23))
            arr_time = dep_time + timedelta(hours=random.randint(1, 4))  # realistic duration

            # Flight details
            airline = random.choice(airlines)
            tier = random.choice(["Economy", "Standard", "Premium"])
            total_seats = random.randint(120, 250)
            available_seats = random.randint(20, total_seats)
            base_price = random.randint(3500, 12000)
            demand = round(random.uniform(0.8, 1.5), 2)

            # Create the record
            Flight.objects.create(
                airline_name=airline,
                origin=origin,
                destination=destination,
                departure_time=dep_time,
                arrival_time=arr_time,
                total_seats=total_seats,
                available_seats=available_seats,
                base_price=base_price,
                airline_tier=tier,
                demand_level=demand
            )

            flights_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {flights_created} future flights!")
        )


