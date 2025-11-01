
from datetime import datetime, timedelta
import random

from django.utils import timezone
from django.utils.dateparse import parse_date


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Booking, Flight, Passenger
from .serializers import BookingSerializer, FlightSerializer, PassengerSerializer,BookingRequestSerializer

from django.shortcuts import render

def index(request):
    source = request.GET.get("source")
    destination = request.GET.get("destination")
    date = request.GET.get("date")
    sort = request.GET.get("sort", "price")

    return render(request, 'flights/index.html', {
        "source": source,
        "destination": destination,
        "date": date,
        "sort": sort,
    })



# Milestone2- dynamic pricing engine

# -----------------------------------------
#  DYNAMIC PRICING ENGINE (Realistic Model)
# -----------------------------------------
def calculate_dynamic_price(base_fare, seats_available, total_seats, departure_time, airline_tier, demand_level):
    """
    Realistic airline dynamic pricing engine.
    Factors:
      - Remaining seat percentage
      - Time until departure
      - Demand level (above 1 = high demand, below 1 = low demand)
      - Airline pricing tier
    """

    #  SEAT AVAILABILITY FACTOR
    seat_ratio = seats_available / total_seats
    if seat_ratio <= 0.2:
        seat_factor = 0.25  # less than 20% seats left → +25%
    elif seat_ratio <= 0.5:
        seat_factor = 0.10  # 50% seats left → +10%
    elif seat_ratio <= 0.8:
        seat_factor = 0.03  # moderate fill → +3%
    else:
        seat_factor = -0.05  # lots of seats left → -5%

    #TIME UNTIL DEPARTURE FACTOR
    days_until_departure = max((departure_time - timezone.now()).days, 0)
    if days_until_departure <= 1:
        time_factor = 0.30  # very close → +30%
    elif days_until_departure <= 3:
        time_factor = 0.15
    elif days_until_departure <= 7:
        time_factor = 0.07
    else:
        time_factor = -0.05  # far away → cheaper

    # DEMAND FACTOR (based on numeric demand level)
    # Normalize demand impact: >1 = increase, <1 = decrease
    if demand_level >= 1.2:
        demand_factor = 0.20  # very high demand
    elif demand_level >= 1.0:
        demand_factor = 0.10  # moderate demand
    elif demand_level >= 0.9:
        demand_factor = 0.0   # normal
    else:
        demand_factor = -0.10  # low demand → lower price

    # AIRLINE TIER FACTOR
    tier_weights = {
        "economy": 0.00,
        "standard": 0.08,
        "business": 0.20,
        "premium": 0.35
    }
    tier_factor = tier_weights.get(airline_tier.lower(), 0.05)

    # TOTAL FACTOR (sum of weighted influences)
    total_factor = seat_factor + time_factor + demand_factor + tier_factor

    # Clamp total factor within realistic airline range (-15% to +60%)
    total_factor = min(max(total_factor, -0.15), 0.60)

    # FINAL PRICE CALCULATION
    dynamic_price = base_fare * (1 + total_factor)

    return round(dynamic_price, 2)


# -----------------------------------------
#  API Endpoint: GET Dynamic Price
# -----------------------------------------
@api_view(['GET'])
def get_dynamic_price(request, flight_id):
    try:
        flight = Flight.objects.get(flight_id=flight_id)
    except Flight.DoesNotExist:
        return Response(
            {"detail": f"Flight with ID {flight_id} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Calculate updated dynamic price
    dynamic_price = calculate_dynamic_price(
        base_fare=flight.base_price,
        seats_available=flight.available_seats,
        total_seats=flight.total_seats,
        departure_time=flight.departure_time,
        airline_tier=flight.airline_tier,
        demand_level=flight.demand_level
    )

    # Return the structured data
    return Response({
        "flight_id": flight.flight_id,
        "airline": flight.airline_name,
        "origin": flight.origin,
        "destination": flight.destination,
        "departure_time": flight.departure_time,
        "arrival_time": flight.arrival_time,
        "base_fare": flight.base_price,
        "dynamic_price": dynamic_price,
        "available_seats": flight.available_seats,
        "total_seats": flight.total_seats,
        "airline_tier": flight.airline_tier,
        "demand_level": flight.demand_level,
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
        data['dynamic_price'] = calculate_dynamic_price(base_fare=f.base_price,
                                                        seats_available=f.available_seats,
                                                        total_seats=f.total_seats,
                                                        departure_time=f.departure_time,
                                                        airline_tier=f.airline_tier,
                                                        demand_level=getattr(f, 'demand_level', None))
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
            "passenger_id": passenger.passenger_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking

@api_view(['GET'])
def get_booked_seats(request):
    flight_id = request.GET.get('flight_id')
    travel_date = request.GET.get('travel_date')

    if not flight_id or not travel_date:
        return Response({
            "status": "failed",
            "message": "Missing flight_id or travel_date"
        }, status=status.HTTP_400_BAD_REQUEST)

    booked_seats = Booking.objects.filter(
        flight_id=flight_id,
        travel_date=travel_date
    ).values_list('seat_no', flat=True)

    return Response({
        "status": "success",
        "booked_seats": list(booked_seats)
    }, status=status.HTTP_200_OK)

from django.shortcuts import render, get_object_or_404
def booking_page(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id)
    
    business_rows = ["1", "2", "3", "4"]
    economy_rows = [str(i) for i in range(5, 16)]
    seat_letters_business = ["A", "B", "C", "D"]
    seat_letters_economy = ["A", "B", "C", "space", "D", "E", "F"]
    booked_seats = ["A1", "B2", "E7"]

    context = {
        "flight": flight,
        "business_rows": business_rows,
        "economy_rows": economy_rows,
        "seat_letters_business": seat_letters_business,
        "seat_letters_economy": seat_letters_economy,
        "booked_seats": booked_seats,
    }
    return render(request, 'flights/create_booking.html', context)


from django.db import transaction
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random

@api_view(['POST'])
def create_booking(request):
    serializer = BookingRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

        passenger_id = data['passenger_id']
        flight_id = data['flight_id']
        requested_seat = data.get('seat_no')

        try:
            with transaction.atomic():  # ensures concurrency safety
                # Lock flight row for update
                flight = Flight.objects.select_for_update().get(flight_id=flight_id)

                # Check flight-level seat availability
                if flight.available_seats <= 0:
                    return Response({
                        "status": "failed",
                        "message": "No seats available for this flight."
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Check seat-level availability
                seat_taken = Booking.objects.filter(
                    flight=flight,
                    travel_date=data['travel_date'],
                    seat_no=requested_seat
                ).exists()

                if seat_taken:
                    return Response({
                        "status": "failed",
                        "message": f"Seat {requested_seat} is already booked. Please choose another."
                    }, status=status.HTTP_409_CONFLICT)

                # Get passenger
                passenger = Passenger.objects.get(passenger_id=passenger_id)

                # Simulated Payment Step
                payment_success = random.random() < 0.8  # 80% chance success
                if not payment_success:
                    return Response({
                        "status": "failed",
                        "message": "Payment failed. Please try again."
                    }, status=status.HTTP_402_PAYMENT_REQUIRED)

                # Calculate dynamic price
                final_price = calculate_dynamic_price(
                    base_fare=flight.base_price,
                    seats_available=flight.available_seats,
                    total_seats=flight.total_seats,
                    departure_time=flight.departure_time,
                    airline_tier=flight.airline_tier,
                    demand_level=flight.demand_level
                )

                # Create booking
                booking = Booking.objects.create(
                    flight=flight,
                    passenger=passenger,
                    travel_date=data['travel_date'],
                    seat_preference=data['seat_preference'],
                    seat_no=requested_seat,
                    total_fare=final_price,
                    status="CONFIRMED"
                )

                # Generate PNR
                booking.pnr = "PNR" + str(booking.booking_id).zfill(9)
                booking.save()

                # Decrement seat safely
                flight.available_seats = F('available_seats') - 1
                flight.save()

                return Response({
                    "status": "success",
                    "message": "Booking confirmed successfully!",
                    "payment_status": "success",
                    "pnr": booking.pnr,
                    "final_price": final_price,
                    "booking_id": booking.booking_id,
                    "booking_details": {
                        "flight": flight.flight_id,
                        "passenger": passenger.name,
                        "date": booking.travel_date,
                        "seat_preference": booking.seat_preference,
                        "seat_no": booking.seat_no,
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
import os
import base64
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Booking
from django.shortcuts import get_object_or_404

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def download_receipt(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # barcode_path = os.path.join(settings.BASE_DIR,'flights', 'static', 'flights', 'images', 'barcode.gif')  # convert GIF -> PNG
    # qr_path = os.path.join(settings.BASE_DIR, 'flights','static', 'flights', 'images', 'qr_code.png')

    context = {
        'booking': booking,
        # 'barcode_url': f"data:image/png;base64,{encode_image(barcode_path)}",
        # 'qr_url': f"data:image/png;base64,{encode_image(qr_path)}",
    }

    html = render_to_string('flights/booking_receipt.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Booking_{booking.booking_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

@api_view(['GET'])
def health_check(request):
    total_flights = Flight.objects.count()
    total_bookings = Booking.objects.count()
    
    return Response({
        "status": "healthy",
        "total_flights": total_flights,
        "total_bookings": total_bookings
    })




import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking

# TELEGRAM_BOT_TOKEN = "7304172250:AAGfhKDi9gmY2eT1CKS0jqepSDWFivYnKeg"
# TELEGRAM_CHAT_ID = "5601751259"  # Can be the passenger’s or admin’s chat

@api_view(['DELETE'])
def cancel_booking(request, pnr):
    try:
        booking = Booking.objects.select_related('flight', 'passenger').get(pnr=pnr.upper())
        flight = booking.flight

        # Restore seat availability
        flight.available_seats += 1
        flight.save()

        cancelled_data = {
            "pnr": booking.pnr,
            "flight_id": flight.flight_id,
            "passenger_id": booking.passenger.passenger_id,
            "seat_no": booking.seat_no,
            "travel_date": booking.travel_date
        }

        # Prepare message for Telegram
        # message = (
        #     f"🛑 *Booking Cancelled Successfully*\n\n"
        #     f"✈️ *PNR:* `{booking.pnr}`\n"
        #     f"🧳 *Flight:* {flight.flight_id}\n"
        #     f"💺 *Seat:* {booking.seat_no}\n"
        #     f"📅 *Date:* {booking.travel_date}\n"
        #     f"👤 *Passenger ID:* {booking.passenger.passenger_id}\n\n"
        #     f"Thank you for using our service!"
        # )

        # Send Telegram notification
        # send_telegram_message(message)

        # Delete booking
        booking.delete()

        return Response({
            "message": "Booking cancelled successfully",
            "cancelled_booking": cancelled_data
        }, status=status.HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response({
            "detail": f"Booking with PNR {pnr.upper()} not found"
        }, status=status.HTTP_404_NOT_FOUND)


# def send_telegram_message(message):
#     """Send message to Telegram chat using bot API"""
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": message,
#         "parse_mode": "Markdown"
#     }
#     try:
#         requests.post(url, data=payload, timeout=5)
#     except Exception as e:
#         print(f"Telegram send failed: {e}")


