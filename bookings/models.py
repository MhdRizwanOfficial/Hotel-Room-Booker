from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Room(models.Model):
    ROOM_TYPES = (
        ('Double Deluxe', 'Double Deluxe Room'),
        ('Double Standard', 'Double Standard Room'),
        ('Honeymoon Suite', 'Honeymoon Suite'),
        ('Economy Double', 'Economy Double'),
    )
    type = models.CharField(max_length=50, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.type



class Booking(models.Model):
    
    STATUS_CHOICES = [
        ('in_cart', 'In Cart'),
        ('completed', 'Completed')
    ]
    
    
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField()
    num_rooms = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_cart')

    
    
    def save(self, *args, **kwargs):
        self.total_price = self.num_rooms * self.price_per_night
        super().save(*args, **kwargs)    




class Availability(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    available_rooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.start_date} to {self.end_date} - {self.available_rooms} rooms"