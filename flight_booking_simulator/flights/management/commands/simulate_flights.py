import asyncio
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from asgiref.sync import sync_to_async
from flights.models import Flight
from flights.views import calculate_dynamic_price  # optional

class Command(BaseCommand):
    help = "Periodically update flight market data (availability & demand)"

    @sync_to_async
    def get_all_flights(self):
        return list(Flight.objects.all())

    @sync_to_async
    def save_flight(self, flight):
        flight.save()

    async def simulate_market_step(self):
        flights = await self.get_all_flights()
        for flight in flights:
            # Random seat fluctuation
            change = random.randint(-3, 3)
            flight.available_seats = max(0, min(flight.total_seats, flight.available_seats + change))

            # Random demand level
            flight.demand_level = round(random.uniform(0.8, 1.5), 2)

            # Optional: recalculate dynamic price
            dynamic_price = calculate_dynamic_price(flight)
            print(f"Flight {flight.flight_id} → ₹{dynamic_price}")

            await self.save_flight(flight)

        print("Market step completed")

    async def scheduler_loop(self, interval_seconds):
        while True:
            await self.simulate_market_step()
            await asyncio.sleep(interval_seconds)

    def handle(self, *args, **kwargs):
        print("Starting flight market simulator...")
        asyncio.run(self.scheduler_loop(300))  # every 5 minutes

# from django.core.management.base import BaseCommand
# from flights.models import Flight


# from datetime import datetime, timedelta
# import random
# from django.utils import timezone

# dep_time = timezone.now() + timedelta(hours=random.randint(2, 72))
# arr_time = dep_time + timedelta(hours=random.randint(1, 4))


# class Command(BaseCommand):
#     help = "Simulate external airline flight data"

#     def handle(self, *args, **kwargs):
#         Flight.objects.all().delete()
#         cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
#         for _ in range(15):
#             origin, destination = random.sample(cities, 2)
#             dep_time = datetime.now() + timedelta(hours=random.randint(2, 72))
#             arr_time = dep_time + timedelta(hours=random.randint(1, 4))
#             base = random.randint(3000, 10000)
#             tier = random.choice(["Economy", "Standard", "Premium"])
#             seats = random.randint(100, 200)
#             available = random.randint(10, seats)
#             demand = round(random.uniform(0.8, 1.5), 2)

#             # Flight.objects.create(
#             #     flight_no=f"AI{random.randint(100,999)}",
#             #     origin=origin,
#             #     destination=destination,
#             #     departure_time=dep_time,
#             #     arrival_time=arr_time,
#             #     base_fare=base,
#             #     total_seats=seats,
#             #     seats_available=available,
#             #     airline_tier=tier,
#             #     demand_level=demand
#             # )

#             Flight.objects.create(
#                 airline_name=random.choice(["IndiGo", "Air India", "SpiceJet"]),
#                 origin=origin,
#                 destination=destination,
#                 departure_time=dep_time,
#                 arrival_time=arr_time,
#                 base_price=base,  # 👈 use base_price instead of base_fare
#                 total_seats=seats,
#                 available_seats=available,
#                 airline_tier=tier,
#                 demand_level=demand
#             )


#         self.stdout.write(self.style.SUCCESS("✅ Simulated flights successfully!"))
