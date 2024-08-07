from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Booking, Room, Availability
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime, timedelta


@login_required
def book_now(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == "POST":
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        num_rooms = int(request.POST.get('num_rooms'))
        price_per_night = Decimal(room.price_per_night)
        
        # Convert check_in and check_out to datetime objects
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        
        # Check room availability for the specified date range
        availability = Availability.objects.filter(
            room=room, 
            start_date__lte=check_in_date, 
            end_date__gte=check_out_date
        )
        available_rooms = min([a.available_rooms for a in availability]) if availability else 0
        
        if num_rooms > available_rooms:
            context = {
                'room': room,
                'check_in': check_in,
                'check_out': check_out,
                'adults': adults,
                'children': children,
                'num_rooms': num_rooms,
                'error_message': f"Only {available_rooms} rooms are available for the selected dates."
            }
            return render(request, 'bookings/book_now.html', context)
        
        # Calculate the total price
        num_nights = (check_out_date - check_in_date).days
        total_price = float(price_per_night) * num_rooms * num_nights

        # Create the booking
        Booking.objects.create(
            user=request.user,
            room_type=room.type,
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            children=children,
            num_rooms=num_rooms,
            price_per_night=price_per_night,
            total_price=total_price,
            booked_at=timezone.now()
        )
        return redirect('bookings:checkout')
    
    # For GET requests, provide default values
    check_in = request.GET.get('check_in', datetime.now().strftime('%Y-%m-%d'))
    check_out = request.GET.get('check_out', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))

    # Fetch the available rooms for the default date range
    availability = Availability.objects.filter(
        room=room, 
        start_date__lte=datetime.now().date(), 
        end_date__gte=(datetime.now() + timedelta(days=1)).date()
    )
    available_rooms = min([a.available_rooms for a in availability]) if availability else 0

    context = {
        'room': room,
        'check_in': check_in,
        'check_out': check_out,
        'adults': 2,  # Default value
        'children': 0,  # Default value
        'num_rooms': 1,  # Default value
        'available_rooms': available_rooms
    }
    return render(request, 'bookings/book_now.html', context)


@login_required
def checkout(request):
    bookings = Booking.objects.filter(user=request.user, status='in_cart')
    return render(request, 'bookings/checkout.html', {'bookings': bookings})

@login_required
def booking_success(request):
    Booking.objects.filter(user=request.user, status='in_cart').update(status='completed')
    return render(request, 'bookings/booking_success.html')


@login_required
def booking_history(request):
    # Fetch booking records for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    
    # Pass the booking records to the template
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})


@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'bookings/room_list.html', {'rooms': rooms})



    
def availability(request):
    availability_list = Availability.objects.all()   
    return render(request, 'bookings/availability.html', {'availability_list': availability_list})

from datetime import datetime
def check_availability(request):
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        # Convert string dates to datetime objects
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        
        # Fetch availability based on the provided dates
        availability_list = Availability.objects.filter(
            start_date__lte=check_out,
            end_date__gte=check_in,
            available_rooms__gt=0
        )
        
        if not availability_list:
            message = "Rooms are not available on these dates."
        else:
            message = ""

        return render(request, 'bookings/check_availability.html', {
            'availability_list': availability_list,
            'message': message,
            'check_in': check_in_date,
            'check_out': check_out_date
        })
    else:
        return render(request, 'bookings/check_availability.html', {'availability_list': [], 'message': ''})
    

def double_deluxe_room(request):
    return render(request, 'rooms/double_deluxe_room.html')

def double_standard_room(request):
    return render(request, 'rooms/double_standard_room.html')

def honeymoon_suite(request):
    return render(request, 'rooms/honeymoon_suite.html')

def economy_double_room(request):
    return render(request, 'rooms/economy_double_room.html')