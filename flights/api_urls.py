# # flights/api_urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     # Flight APIs
#     path('flights/search/', views.search_flights, name='search_flights_api'),
#     path('flights/', views.list_flights, name='list_flights_api'),
#     path('flights/<int:flight_id>/', views.flight_detail, name='flight_detail_api'),
#     path('flights/filter/', views.filter_flights, name='filter_flights_api'),
#     path('flights/airlines/', views.get_all_airlines, name='get_all_airlines_api'),
#     path('flights/dynamic-price/<int:flight_id>/', views.get_dynamic_price, name='get_dynamic_price_api'),

#     # Booking APIs
#     path('booking/<int:booking_id>/', views.fetch_all_booking, name='fetch_booking_api'),
#     path('bookings/', views.create_booking, name='create_booking_api'),
#     path('bookings/<str:pnr>/', views.cancel_booking, name='cancel_booking_api'),
#     path('booking/<int:booking_id>/receipt/', views.download_receipt, name='download_receipt_api'),
#     path('booked-seats/', views.get_booked_seats, name='get_booked_seats_api'),

#     # Passenger API
#     path('passengers/', views.create_passenger, name='create_passenger_api'),

#     # System
#     path('health/', views.health_check, name='health_check_api'),

#     # Auth APIs (for AJAX requests)
#     path('auth/login/', views.login_api, name='login_api'),
#     path('auth/signup/', views.signup_api, name='signup_api'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('flights/search/', views.search_flights),
    path('flights/', views.list_flights),
    path('flights/<int:flight_id>/', views.flight_detail),
    path('flights/filter/', views.filter_flights),
    path('flights/airlines/', views.get_all_airlines, name='get_all_airlines_api'),
    path('booking/<int:booking_id>/', views.fetch_all_booking),
    path('passengers/', views.create_passenger),
    path('bookings/', views.create_booking),
    path('booked-seats/', views.get_booked_seats, name='get_booked_seats'),
    path('booking/<int:booking_id>/receipt/', views.download_receipt, name='download_receipt'),
    path('health/', views.health_check),
    path('bookings/<str:pnr>/', views.cancel_booking),
    path('dynamic_price/<int:flight_id>/', views.get_dynamic_price),

    # # Auth API routes
    # path('login/', views.login_page, name='login_page'),
    # path('signup/', views.signup_page, name='signup_page'),
    # path('logout/', views.logout_view, name='logout'),
    # # path('dashboard/', views.dashboard, name='dashboard'),

    # path('api/login/', views.login_api, name='login_api'),
    # path('api/signup/', views.signup_api, name='signup_api'),
]


