from django.shortcuts import render,reverse,redirect
from django.contrib.auth import authenticate ,login as auth_Login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY
from users.models import *
from travelers.models import *
from web.form import *


















def index(request):
    destinations = Destination.objects.all()[:3] 

    context = {
        'destinations': destinations
    }

    return render(request, 'web/index.html', context=context)




def spotlight_list(request):
    spotlights = Spotlight.objects.all()
    context= {
        'spotlights': spotlights
    }
    return render(request, 'web/spotlight_list.html',context=context)

def spotlight_detail(request, id):
    spotlight = get_object_or_404(Spotlight, id=id)

    context = {
        'spotlight': spotlight
        }
    return render(request, 'web/spotlight_detail.html', context=context)


def travelers_choice_list(request):
    
    choices = TravelersChoice.objects.filter(featured=True)

    context = {
        'choices': choices
    }
    return render(request, 'web/traveler_choice_list.html' ,context=context)


def travelers_choice_detail(request, id):
    choice = get_object_or_404(TravelersChoice, id=id)
    context = {
        'choice': choice
    }
    return render(request, 'web/traveler-choice.html',context=context) 



def categories_and_destinations(request):
    category_choices = [('all', 'All')] + (Destination.CATEGORY_CHOICES)
    selected_category = request.GET.get('category', 'all')  

    if selected_category == 'all':
        destinations = Destination.objects.all()
    else:
        destinations = Destination.objects.filter(category=selected_category)
        context = {
            'destinations': destinations,
            'category_choices': category_choices,
            'selected_category': selected_category,
        }

    return render(request, 'web/categories.html',context=context)



    
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(email=email).exists():
            context = {
                'error': True,
                'message': 'Email already exists'
            }
            return render(request, 'web/register.html', context=context)
        
       
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        
        customer = Customer.objects.create(user=user)
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




from decimal import Decimal

def booking_amount_minor_units(booking):
    # Get the price of the destination
    price = Decimal(booking.destination.price)

    # Multiply by number of people
    total = price * booking.num_people

    # Convert to paise (multiply by 100) and return as integer
    return int(total * 100)


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

        # 🔹 Calculate amount (minor units)
        amount_minor = booking_amount_minor_units(booking)

        # 🔹 Success + cancel URLs
        success_url = settings.SITE_URL + reverse('web:success') + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = settings.SITE_URL + reverse('web:cancel')

        # 🔹 Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': settings.STRIPE_CURRENCY,
                    'unit_amount': amount_minor,
                    'product_data': {
                         'name': f"{destination.title} × {num_people}",
                         'description': f"Booking #{booking.id} for {travel_date}",
                    },
                },
                'quantity': 1,
            }],
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=request.user.email,
            metadata={'booking_id': str(booking.id)},
            idempotency_key=f'booking-{booking.id}',
        )

        # 🔹 Save payment intent ID + amount in Booking
        booking.payment_intent_id = session.payment_intent
        booking.amount_paid = amount_minor
        booking.save(update_fields=['payment_intent_id', 'amount_paid'])

        # 🔹 Redirect user to Stripe Checkout (no JS needed)
        return HttpResponseRedirect(session.url, status=303)

    return render(request, "web/book_dest.html", {"destination": destination})


def checkout_success(request):
    """
    Stripe sends back ?session_id=xxx
    We'll verify it and mark the Booking as paid.
    """
    session_id = request.GET.get("session_id")
    context = {"paid": False}

    if session_id:
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent_id = session.payment_intent
        booking_id = (session.metadata or {}).get("booking_id")

        if booking_id:
            booking = Booking.objects.filter(id=booking_id).first()
            if booking:
                # Double-check payment status
                pi = stripe.PaymentIntent.retrieve(payment_intent_id)
                if pi.status == "succeeded":
                    booking.is_paid = True
                    booking.payment_intent_id = payment_intent_id
                    booking.amount_paid = session.amount_total  # Stripe gives in minor units
                    booking.save(update_fields=["is_paid", "payment_intent_id", "amount_paid"])

                    context.update({"paid": True, "booking": booking})

    return render(request, "web/success.html", context)
    
def cancel_booking(request):
    # You can show a simple cancel page
    return render(request, "web/cancel.html")



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








