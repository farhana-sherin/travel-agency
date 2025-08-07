from django.shortcuts import render,reverse
from django.contrib.auth import authenticate ,login as auth_Login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



from users.models import *
from travelers.models import *
from web.form import *


def index(request):
    pass
    return render(request,'web/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_Login(request, user)
            return HttpResponseRedirect(reverse('web:index'))  
        else:
            context={

                'error':True,
                'message':'invalid email or password'


       
            }
            return render(request, 'web/login.html', context=context)
    else:
        return render(request,'web/login.html')



def register(request):
    if request.method == 'POST':
      
        email = request.POST.get('email')
        password = request.POST.get('password')
      

        if User.objects.filter(email=email).exists():
            context = {
                'error': True,
                'message': 'Email already exists'
            }
            return render(request, 'web/register.html',context=context)
        else:
            user = User.objects.create_user(
                
                email=email,
                password=password,
                
               
            )
            user.save()

            customer = Customer.objects.create(
                user=user
            )
            customer.save()
           
            return HttpResponseRedirect(reverse('web:login'))
    else:
        return render(request, 'web/register.html')
    

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('web:login'))



def destination_list(request):
    destinations = Destination.objects.all()
    context = {
        'destinations': destinations
    }
    return render(request, 'web/destination.html', context=context)



def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)  
    context = {
        'destination': destination
    }
    return render(request, 'web/destination_detail.html', context=context)




@login_required
def book_destination(request, id):
    user = request.user
    customer= Customer.objects.get(user=user)
    destination = get_object_or_404(Destination, id=id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer
            booking.destination = destination
            booking.save()
            return HttpResponseRedirect(reverse('web:booking_success'))
    else:
        form = BookingForm()

    context = {
        'destination': destination,
        'form': form,
        'customer': customer,
    }
    return render(request, 'web/book_dest.html', context)


    

    
def booking_success(request):
    return render(request, 'web/booking_success.html')



@login_required
def bookings(request):
    user= request.user
    customer = Customer.objects.get(user=user)
    bookings = Booking.objects.filter(customer=customer)
    
    context = {
        'bookings': bookings
    }   
    return render(request, 'web/booking.html',context=context)


@login_required
def booking_detail(request, id):
    user = request.user
    customer =Customer.objects.get(user=user)
    booking = Booking.objects.get(id=id,customer=customer)

    context = {
        'booking': booking
    }
    return render(request, 'web/booking_detail.html', context)



