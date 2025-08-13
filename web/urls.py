from django.urls import path
from web import views


app_name="web"

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name="login"),
    path('destinations/', views.destination_list, name='destination_list'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('destination/<int:id>/', views.destination_detail, name='destination_detail'),
    path('destination/<int:id>/book/', views.book_destination, name='book_destination'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.bookings, name='bookings'),
    path('booking/<int:id>/', views.booking_detail, name='booking_detail'),
    
    
    path('payment/<int:id>/', views.payment, name='payment'),
    path('spotlights/', views.spotlight_list, name='spotlight_list'),
    path('spotlights/<int:id>/', views.spotlight_detail, name='spotlight_detail'),
    path('travelers-choice/', views.travelers_choice_list, name='travelers_choice_list'),
    path('travelers-choice/<int:id>/', views.travelers_choice_detail, name='travelers_choice_detail'),
    path('categories/', views.categories_and_destinations, name='categories_and_destinations'),
    path('travelers-choice/add/', views.add_travelers_choice, name='add_travelers_choice'),

]