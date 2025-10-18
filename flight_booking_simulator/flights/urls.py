from django.urls import path
from . import views

urlpatterns = [

    path('flights/search/', views.search_flights),
    path('flights/', views.list_flights),
    path('flights/<int:flight_id>/', views.flight_detail),
    path('flights/filter/', views.filter_flights),
    path('airline_names/', views.get_all_airlines),
    path('booking/<int:booking_id>/', views.fetch_all_booking),
    path('passengers/', views.create_passenger),
    path('bookings/', views.create_booking),
    path('health/', views.health_check),
    path('bookings/<str:pnr>/', views.cancel_booking),
    path('dynamic_price/<int:flight_id>/', views.get_dynamic_price),

]
