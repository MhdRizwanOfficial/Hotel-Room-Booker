from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from bookings.models import Room

def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about.html')

def accomodation(request):
    rooms = Room.objects.all()
    return render(request, 'bookings/accommodation.html', {'rooms': rooms})

def gallery(request):
    return render(request, 'gallery.html')

def contact(request):
    return render(request, 'contact.html')
