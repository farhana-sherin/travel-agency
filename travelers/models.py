from django.db import models

from users.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    class Meta:
        db_table='customer_users'
        verbose_name='customer'
        verbose_name_plural='customers'
        ordering=['-id']


    def __str__(self):
        return self.user.email
    

class Spotlight(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='spotlight_images/')

    def __str__(self):
        return self.title
    
class TravelersChoice(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    short_description = models.TextField()
    full_description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    image = models.ImageField(upload_to='travelers_choice/')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    




class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('beach', 'Beach Getaway'),
        ('mountain', 'Mountain Adventure'),
        ('city', 'City Escape'),
        ('desert', 'Desert Safari'),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='beach')
    location = models.CharField(max_length=100) 
    description = models.TextField() 
    price = models.FloatField()
    image = models.ImageField(upload_to='destinations/')
    duration = models.CharField(max_length=50)  

    class Meta:
        db_table = 'destination_list'
        verbose_name = 'destination'
        verbose_name_plural = 'destinations'
        ordering = ['-id']

    def __str__(self):
        return self.title


class DestinationDetail(models.Model):
    destination = models.OneToOneField(Destination, on_delete=models.CASCADE, related_name='extra_details')
    plan = models.TextField(blank=True, null=True)  #
    notes = models.TextField(blank=True, null=True) 

    class Meta:
        db_table = 'destination_detail'
        verbose_name = 'destination detail'
        verbose_name_plural = 'destination details'
        ordering=['-id']

    def __str__(self):
         return self.destination.title
    



class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    travel_date = models.DateField()
    num_people = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)  # Stripe PaymentIntent ID
    amount_paid = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'booking'
        verbose_name = 'booking detail'
        verbose_name_plural = 'booking details'
        ordering = ['-id']

    def __str__(self):
        return self.customer.user.email

