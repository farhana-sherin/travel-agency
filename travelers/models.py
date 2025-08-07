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
    


class Destination(models.Model):
    title = models.CharField(max_length=100)
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


    class Meta:
        db_table = 'booking'
        verbose_name = 'booking detail'
        verbose_name_plural = 'booking details'
        ordering = ['-id']

    def __str__(self):
        return self.customer.user.email

