from django.shortcuts import render,reverse
from django.contrib.auth import authenticate ,login as auth_Login, logout as auth_logout
from django.http import HttpResponseRedirect


from users.models import User
from travelers.models import Customer


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
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

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
    pass
    return render(request, 'web/destination.html')



