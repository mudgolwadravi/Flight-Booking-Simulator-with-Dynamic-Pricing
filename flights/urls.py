# from django.urls import path
# from django.shortcuts import render
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('flights/search/', views.search_flights),
#     path('flights/search-page/', lambda request: render(request, 'flights/search_flights.html'), name='search_page'),
#     path('flights/', views.list_flights),
#     path('flights/list-page/', lambda request: render(request, 'flights/list_flights.html'), name='list_page'),
#     path('flights/<int:flight_id>/', views.flight_detail),
#     path('flights/detail-page/<int:flight_id>/', lambda request, flight_id: render(request, 'flights/flight_detail.html', {'flight_id': flight_id}), name='flight_detail_page'),
#     path('flights/filter/', views.filter_flights),
#     path('flights/filter-page/',lambda request: render(request, 'flights/filter_flights.html'),name='filter_flights_page'),
#     # path('airline_names/', views.get_all_airlines),
#     path('flights/airlines/', views.get_all_airlines, name='get_all_airlines_api'),
#     path('airlines_page/', lambda request: render(request, 'flights/airlines_list.html'), name='airlines_list_page'),
#     path('booking/<int:booking_id>/', views.fetch_all_booking),
#     path('passengers/', views.create_passenger),
#     path('passengers-page/', lambda request: render(request, 'flights/create_passenger.html'), name='create_passenger_page'),
#     path('bookings/', views.create_booking),
#     path('booked-seats/', views.get_booked_seats, name='get_booked_seats'),
#     path('bookings-page/<int:flight_id>/', views.booking_page, name='booking_page'),
#     path('booking/<int:booking_id>/receipt/', views.download_receipt, name='download_receipt'),
#     path('bookings-page/<int:flight_id>/', views.create_booking, name='create_booking_page'),
#     path('health/', views.health_check),
#     path('bookings/<str:pnr>/', views.cancel_booking),
#     path('cancel-booking-page/', lambda request: render(request, 'flights/cancel_booking.html'), name='cancel_booking_page'),
#     path('dynamic_price/<int:flight_id>/', views.get_dynamic_price),

#     path('login/', views.login_page, name='login_page'),
#     path('signup/', views.signup_page, name='signup_page'),
#     path('logout/', views.logout_view, name='logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),

# ]


from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'flights/index.html'), name='search_page'),
    path('flights/search-page/', lambda request: render(request, 'flights/search_flights.html'), name='search_page'),
    path('flights/list-page/', lambda request: render(request, 'flights/list_flights.html'), name='list_page'),
    path('flights/detail-page/<int:flight_id>/', lambda request, flight_id: render(request, 'flights/flight_detail.html', {'flight_id': flight_id}), name='flight_detail_page'),
    path('flights/filter-page/', lambda request: render(request, 'flights/filter_flights.html'), name='filter_flights_page'),
    path('airlines_page/', lambda request: render(request, 'flights/airlines_list.html'), name='airlines_list_page'),
    path('passengers-page/', lambda request: render(request, 'flights/create_passenger.html'), name='create_passenger_page'),
    path('bookings-page/<int:flight_id>/', lambda request, flight_id: render(request, 'flights/booking.html', {'flight_id': flight_id}), name='booking_page'),
    path('cancel-booking-page/', lambda request: render(request, 'flights/cancel_booking.html'), name='cancel_booking_page'),
]
