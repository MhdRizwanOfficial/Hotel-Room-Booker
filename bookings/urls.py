from django.urls import path
from . import views

app_name = 'bookings' 

urlpatterns = [
    path('book-now/<int:room_id>/', views.book_now, name='book_now'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('booking-success/', views.booking_success, name='booking_success'),
    # path('room-list/', views.room_list, name='room_list'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('room_availability/', views.availability, name='availability'),
    path('booking-history/', views.booking_history, name='booking_history'), 
    path('rooms/double-deluxe/', views.double_deluxe_room, name='double_deluxe_room'),
    path('rooms/double-standard/', views.double_standard_room, name='double_standard_room'),
    path('rooms/honeymoon-suite/', views.honeymoon_suite, name='honeymoon_suite'),
    path('rooms/economy-double/', views.economy_double_room, name='economy_double_room'),   
]
