from django.contrib import admin
from .models import Room, Booking, Availability

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['type', 'price_per_night']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'check_in', 'check_out', 'num_rooms', 'total_price', 'booked_at']


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['room', 'start_date', 'end_date', 'available_rooms', 'price']