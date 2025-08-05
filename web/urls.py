from django.urls import path
from web import views


app_name="web"

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name="login"),
    path('destinations/', views.destination_list, name='destination_list'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]