
from datetime import datetime, timedelta
import random

from django.utils import timezone
from django.utils.dateparse import parse_date


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Booking, Flight, Passenger
from .serializers import BookingSerializer, FlightSerializer, PassengerSerializer,BookingRequestSerializer




# --- Dynamic Pricing Logic ---
# Milestone2- dynamic pricing engine


def calculate_dynamic_price(base_fare, seats_available, total_seats, departure_time, airline_tier, demand_level=None):
    """
    Calculates dynamic flight price based on seat availability, time to departure,
    demand level, and airline tier.
    """

    # 1. Seat Factor
    seat_ratio = seats_available / total_seats
    seat_factor = (1 - seat_ratio) * 0.3  # fewer seats → higher price

    # 2. Time Factor
    days_until_departure = (departure_time - timezone.now()).days
    days_until_departure = max(days_until_departure, 0)
    time_factor = (1 / (days_until_departure + 1)) * 0.5  # closer → more expensive

    # 3. Demand Factor
    if demand_level is None:
        demand_factor = random.uniform(-0.1, 0.3)  # simulate real-time demand
    else:
        demand_factor = demand_level

    # 4. Tier Factor
    tier_weights = {
        "economy": 0.0,
        "standard": 0.2,
        "business": 0.3,
        "premium": 0.4
    }
    tier_factor = tier_weights.get(airline_tier.lower(), 0.1)

    # 5. Total Factor
    total_factor = seat_factor + time_factor + demand_factor + tier_factor
    dynamic_price = base_fare * (1 + total_factor)

    return round(dynamic_price, 2)


@api_view(['GET'])
def get_dynamic_price(request, flight_id):
    try:
        flight = Flight.objects.get(flight_id=flight_id)
    except Flight.DoesNotExist:
        return Response(
            {"detail": f"Flight with ID {flight_id} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Calculate dynamic price
    price = calculate_dynamic_price(base_fare=flight.base_price,
        seats_available=flight.available_seats,
        total_seats=flight.total_seats,
        departure_time=flight.departure_time,
        airline_tier=flight.airline_tier,
        demand_level=flight.demand_level  # optional
    )

    return Response({
        "flight_id": flight.flight_id,
        "origin": flight.origin,
        "destination": flight.destination,
        "departure_time": flight.departure_time,
        "arrival_time": flight.arrival_time,
        "base_fare": flight.base_price,
        "dynamic_price": price,
        "seats_available": flight.available_seats,
        "total_seats": flight.total_seats,
        "airline_tier": flight.airline_tier,
        "demand_level": flight.demand_level
    }, status=status.HTTP_200_OK)


# --- Search Flights ---

@api_view(['GET'])
def search_flights(request):
    """
    Search for flights by origin, destination, and date with validation and sorting.
    Example: /api/flights/search/?origin=Delhi&destination=Mumbai&date=2025-10-20&sort=price
    """
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date_str = request.GET.get('date')
    sort_by = request.GET.get('sort', 'price').lower()  # default to price

    # -----------------------
    # Input Validation
    # -----------------------
    errors = {}

    if not origin:
        errors['origin'] = "Origin city is required."
    if not destination:
        errors['destination'] = "Destination city is required."
    if not date_str:
        errors['date'] = "Travel date (YYYY-MM-DD) is required."

    # Parse and validate date format
    try:
        travel_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        errors['date'] = "Invalid date format. Use YYYY-MM-DD."

    if origin and destination and origin.lower() == destination.lower():
        errors['destination'] = "Origin and destination cannot be the same."

    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    # -----------------------
    # Query Flights
    # -----------------------
    flights = Flight.objects.filter(
        origin__iexact=origin,
        destination__iexact=destination,
        departure_time__date=travel_date
    )

    if not flights.exists():
        return Response({"message": "No flights found for the given criteria."}, status=404)

    # -----------------------
    # Attach Dynamic Prices + Duration
    # -----------------------
    flight_data = []
    for f in flights:
        data = FlightSerializer(f).data
        data['dynamic_price'] = calculate_dynamic_price(f)
        data['duration_hours'] = round((f.arrival_time - f.departure_time).total_seconds() / 3600, 2)
        flight_data.append(data)

    # -----------------------
    #  Sorting
    # -----------------------
    if sort_by == 'price':
        flight_data.sort(key=lambda x: x['dynamic_price'])
    elif sort_by == 'duration':
        flight_data.sort(key=lambda x: x['duration_hours'])
    else:
        return Response(
            {"error": "Invalid sort parameter. Use 'price' or 'duration'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------
    # Return Response
    # -----------------------
    return Response({
        "total_results": len(flight_data),
        "sort_by": sort_by,
        "flights": flight_data
    })




@api_view(['GET'])
def list_flights(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def flight_detail(request, flight_id):
    try:
        flight = Flight.objects.get(flight_id=flight_id)
        serializer = FlightSerializer(flight)
        return Response(serializer.data)
    except Flight.DoesNotExist:
        return Response({'error':'Flight not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def filter_flights(request):
    max_price = int(request.GET.get('max_price', 10000))
    direct_only = request.GET.get('direct_only', 'false').lower() == 'true'
    airline_name = request.GET.get('airline_name')

    flights = Flight.objects.filter(base_price__lte=max_price)

    if direct_only:
        flights = flights.filter(total_seats=flights.available_seats)  # Assuming direct flights have no layovers

    if airline_name:
        flights = flights.filter(airline_name__iexact=airline_name)

    serializer = FlightSerializer(flights, many=True)
    filters_applied = {
        "max_price": max_price,
        "direct_only": direct_only,
        "airline_name": airline_name if airline_name else "All airlines"
    }

    return Response({
        "filters_applied": filters_applied,
        "results": serializer.data
    })

@api_view(['GET'])
def get_all_airlines(request):
    airlines = (
        Flight.objects
        .values('airline_name')
        .distinct()
    )

    # Optional: map to a custom format if needed
    airline_list = [
        {"flight_id": f"{airline['airline_name'][:2].upper()}", "name": airline['airline_name']}
        for airline in airlines
    ]

    return Response(airline_list)



@api_view(['GET'])
def fetch_all_booking(request, booking_id):
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def create_passenger(request):
    serializer = PassengerSerializer(data=request.data)
    if serializer.is_valid():
        passenger = serializer.save()
        return Response({
            "message": "Passenger details are created successfully",
            "passenger_id": passenger.id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.db import transaction
from django.db.models import F

@api_view(['POST'])
def create_booking(request):
    serializer = BookingRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

        passenger_id = data['passenger_id']
        flight_id = data['flight_id']

        try:
            with transaction.atomic():  # ensures concurrency safety
                # Lock flight row for update
                flight = Flight.objects.select_for_update().get(id=flight_id)

                # Check seat availability
                if flight.available_seats <= 0:
                    return Response({
                        "status": "failed",
                        "message": "No seats available for this flight."
                    }, status=status.HTTP_400_BAD_REQUEST)

                passenger = Passenger.objects.get(id=passenger_id)

                # --- Simulated Payment Step ---
                payment_success = random.random() < 0.8  # 80% chance success

                if not payment_success:
                    return Response({
                        "status": "failed",
                        "message": "Payment failed. Please try again."
                    }, status=status.HTTP_402_PAYMENT_REQUIRED)

                # --- Calculate dynamic price ---
                final_price = calculate_dynamic_price(
                    base_fare=flight.base_price,
                    seats_available=flight.available_seats,
                    total_seats=flight.total_seats,
                    departure_time=flight.departure_time,
                    airline_tier=flight.airline_tier,
                    demand_level=flight.demand_level
                )

                # --- Create booking ---
                booking = Booking.objects.create(
                    flight=flight,
                    passenger=passenger,
                    travel_date=data['travel_date'],
                    seat_preference=data['seat_preference'],
                    price=final_price,
                    status="CONFIRMED"
                )

                # --- Generate PNR ---
                booking.pnr = "PNR" + str(booking.id).zfill(9)
                booking.save()

                # --- Decrement seat safely ---
                flight.available_seats = F('available_seats') - 1
                flight.save()

                return Response({
                    "status": "success",
                    "message": "Booking confirmed successfully!",
                    "payment_status": "success",
                    "pnr": booking.pnr,
                    "final_price": final_price,
                    "booking_details": {
                        "flight": flight.flight_id,
                        "passenger": passenger.name,
                        "date": booking.travel_date,
                        "seat_preference": booking.seat_preference,
                        "price": final_price
                    }
                }, status=status.HTTP_201_CREATED)

        except Flight.DoesNotExist:
            return Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)
        except Passenger.DoesNotExist:
            return Response({"error": "Passenger not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def health_check(request):
    total_flights = Flight.objects.count()
    total_bookings = Booking.objects.count()
    
    return Response({
        "status": "healthy",
        "total_flights": total_flights,
        "total_bookings": total_bookings
    })



@api_view(['DELETE'])
def cancel_booking(request, pnr):
    try:
        booking = Booking.objects.select_related('flight').get(pnr=pnr.upper())

        # Restore seat availability
        flight = booking.flight
        flight.seats_available += 1
        flight.save()

        # Capture cancelled booking details
        cancelled_data = {
            "pnr": booking.pnr,
            "flight_id": flight.id,
            "passenger_id": booking.passenger.id,
            "seat_no": booking.seat_no,
            "travel_date": booking.travel_date
        }

        # Delete the booking
        booking.delete()

        return Response({
            "message": "Booking cancelled successfully",
            "cancelled_booking": cancelled_data
        }, status=status.HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response({
            "detail": f"Booking with PNR {pnr.upper()} not found"
        }, status=status.HTTP_404_NOT_FOUND)



