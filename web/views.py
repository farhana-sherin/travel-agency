from django.shortcuts import render,reverse,redirect
from django.contrib.auth import authenticate ,login as auth_Login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

import datetime
from django.utils import timezone








from users.models import *
from travelers.models import *
from web.form import *


















def index(request):
    destinations = Destination.objects.all()[:3] 

    context = {
        'destinations': destinations
    }

    return render(request, 'web/index.html', context)




def spotlight_list(request):
    spotlights = Spotlight.objects.all()
    return render(request, 'web/spotlight_list.html', {'spotlights': spotlights})

def spotlight_detail(request, id):
    spotlight = get_object_or_404(Spotlight, id=id)
    return render(request, 'web/spotlight_detail.html', {'spotlight': spotlight})



def travelers_choice_list(request):
    
    choices = TravelersChoice.objects.filter(featured=True)
    return render(request, 'web/traveler_choice_list.html', {'choices': choices})


def travelers_choice_detail(request, id):
    choice = get_object_or_404(TravelersChoice, id=id)
    return render(request, 'web/traveler-choice.html', {'choice': choice})



def categories_and_destinations(request):
    category_choices = [('all', 'All')] + list(Destination.CATEGORY_CHOICES)
    selected_category = request.GET.get('category', 'all')  

    if selected_category == 'all':
        destinations = Destination.objects.all()
    else:
        destinations = Destination.objects.filter(category=selected_category)

    return render(request, 'web/categories.html', {
        'categories': category_choices,
        'selected_category': selected_category,
        'destinations': destinations
    })



    
@login_required
def add_travelers_choice(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        short_description = request.POST.get('short_description')
        full_description = request.POST.get('full_description')
        rating = request.POST.get('rating') or 5.0
        image = request.FILES.get('image')

        TravelersChoice.objects.create(
            name=name,
            location=location,
            short_description=short_description,
            full_description=full_description,
            rating=rating,
            image=image,
            featured=True,
        )
        return HttpResponseRedirect(reverse('web:travelers_choice_list'))

    return render(request, 'web/add_traveler_choice.html')

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
    destination = get_object_or_404(Destination, id=id)
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == "POST":
        travel_date = request.POST.get("travel_date")
        num_people = int(request.POST.get("num_people"))

        booking = Booking.objects.create(
            customer=customer,
            destination=destination,
            travel_date=travel_date,
            num_people=num_people
        )

        # Redirect straight to payment
        return redirect(reverse('web:payment', kwargs={'id': booking.id}))

    return render(request, "web/book_dest.html", {"destination": destination})

@login_required
def payment(request, id):
    booking = get_object_or_404(Booking, id=id, customer__user=request.user)

    return render(request, "web/payment.html", {
        "booking": booking,
       
    })




    

    
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

        'booking': booking,
         
        
    }
    
    return render(request, 'web/booking_detail.html', context=context)








